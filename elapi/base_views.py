from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView as BaseAPIView

from .exceptions import *


class APIView(BaseAPIView):
    """
    Base class for all APIViews. Provides certain enhancements
    for usual process flows. Inspired by GenericAPIView but uses
    marshmallow conventions
    """

    # You'll need to either set these attributes,
    # or override `get_queryset()`/`get_schema_class()`.
    # If you are overriding a view method, it is important that you call
    # `get_queryset()` instead of accessing the `queryset` property directly,
    # as `queryset` will get evaluated only once, and those results are cached
    # for all subsequent requests.
    queryset = None
    schema_class = None

    # If you want to use object lookups other than pk, set 'lookup_field'.
    # For more complex lookup requirements override `get_object()`.
    lookup_field = 'pk'
    lookup_url_kwarg = None

    # The below flags state the mode of operation on (many or single) objects
    # for different methods. Basis the flow handles operation for single or
    # many objects.
    post_many = False
    put_many = False
    patch_many = False
    delete_many = False
    partial_consume = False

    # The filter backend classes to use for queryset filtering
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS

    # The style to use for queryset pagination.
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def initial_processing(self):
        """
        This method can be used as initial processing in different request
        method calls. All builtin child API classes invoke this method
        as the first step.

        One can override the method and perform any initial processing
        common across different request calls if builtin API classes
        are being used
        """
        pass

    def get_queryset(self):
        """
        Get the list of items for this view.
        This must be an iterable, and may be a queryset.
        Defaults to using `self.queryset`.

        This method should always be used rather than accessing `self.queryset`
        directly, as `self.queryset` gets evaluated only once, and those results
        are cached for all subsequent requests.

        You may want to override this if you need to provide different
        querysets depending on the incoming request.
        """
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        try:
            obj = get_object_or_404(queryset, **filter_kwargs)
        except:
            field = self.lookup_field
            raise DataNotFoundException('%s does not exist' % queryset.model.__name__, field)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj

    def filter_queryset(self, queryset):
        """
        Given a queryset, filter it with whichever filter backend is in use.

        You are unlikely to want to override this method, although you may need
        to call it either from a list view, or from a custom `get_object`
        method if you want to apply the configured filtering backend to the
        default queryset.
        """
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def process_list_queryset(self, qs):
        """
        Perform any addition processing on queryset after `filter_queryset` for
        listing.

        Mainly to be used for ListView to populate list if queryset does not meet
        the requirements.
        """
        return qs

    def get_payload(self):
        """
        Returns the payload data sent in the request. The data is used
        by schema for deserilization.

        Returns `request.data` by default
        """
        return self.request.data

    def get_schema(self, *args, **kwargs):
        """
        Return the schema instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        schema_class = self.get_schema_class()
        extra_kwargs = self.get_schema_kwargs()
        kwargs.update(extra_kwargs)
        return schema_class(*args, **kwargs)

    def get_schema_class(self):
        """
        Return the class to be used as Schema.
        Defaults to using `self.schema_class`.
        """
        assert self.schema_class is not None, (
            "'%s' should either include a `schema_class` attribute, "
            "or override the `get_schema_class()` method."
            % self.__class__.__name__
        )
        return self.schema_class

    def get_schema_kwargs(self):
        """
        Extra kwargs provided to the serializer class.
        """
        kwargs = {}
        kwargs['context'] = {'request': self.request}
        return kwargs

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get_dump_data(self, qs, **kwargs):
        """
        Serializes a queryset or object.

        Takes `many` as the only argument and fetches Queryset using
        `get_queryset` method or Object using `get_object` method depending on
        the value.

        Returns the final serialized data using the `dump` method
        of the schema fetched using `get_schema` method.
        """
        schema = self.get_schema(**kwargs)
        data = schema.dump(qs)
        return data

    def get_load_data(self, data, **kwargs):
        """
        Deserializes the data structure in `request.data` .

        Uses `get_schema` method to fetch the schema and uses
        the `load` method of schema to validate the data.

        Returns the Deserialized data or raises ValidationError
        """
        schema = self.get_schema(**kwargs)

        # Finally load and check for errors and return data
        try:
            data = schema.load(data)
        except ValidationError as err:
            raise ValidationError(err)
        return data


class ListView(APIView):
    """
    View to return list of records
    """
    def get(self, request, *args, **kwargs):
        # Initial Processing method invoked
        self.initial_processing()
        # Fetch initial queryset
        qs = self.filter_queryset(self.get_queryset())
        # Perform addition processing on queryset for listing
        qs = self.process_list_queryset(qs)
        # Check and execute pagination process
        page = self.paginate_queryset(qs)
        if page is not None:
            data = self.get_dump_data(page, many=True)
            return self.get_paginated_response(data)
        # Incase of disabled pagination return normal results
        data = self.get_dump_data(qs, many=True)
        return Response(data, status=status.HTTP_200_OK)


class RetrieveView(APIView):
    """
    View to fetch and return one record
    """
    def get(self, request, *args, **kwargs):
        # Initial Processing method invoked
        self.initial_processing()
        # Fetch object
        instance = self.get_object()
        # Get serialized data and return response
        data = self.get_dump_data(instance)
        return Response(data, status=status.HTTP_200_OK)


class CreateView(APIView):
    """
    View to create one or list of records. Subclass is
    supposed to override the perform_create method and
    handle db processing and return appropriate data
    that is sent out as API Response data
    """
    post_status_code = status.HTTP_201_CREATED

    def post(self, request, *args, **kwargs):
        # Initial Processing method invoked
        self.initial_processing()
        # Get initial payload to be validated
        payload = self.get_payload()
        # Get validated data from schema
        data = self.get_load_data(data=payload, many=self.post_many)
        # Invoke create method
        resp_data = self.perform_create(data)
        # Return response
        return Response(resp_data, status=self.post_status_code)

    def perform_create(self, data):
        raise NotImplementedError


class UpdateView(APIView):
    """
    View to update one more more records. Subclass is
    supposed to override the perform_update method and
    handle db processing and return appropriate data
    that is sent out as API Response data
    """
    put_status_code = status.HTTP_200_OK
    patch_status_code = status.HTTP_200_OK

    def put(self, request, *args, **kwargs):
        # Initial Processing method invoked
        self.initial_processing()
        # Get initial payload to be validated
        payload = self.get_payload()
        # Get validated data from schema
        data = self.get_load_data(data=payload, many=self.put_many)
        # Check for many/single processing and pass instance accordingly
        if self.put_many:
            instance = None
        else:
            instance = self.get_object()
        # Invoke update method
        resp_data = self.perform_update(instance, data)
        # Return response
        return Response(resp_data, status=self.put_status_code)

    def patch(self, request, *args, **kwargs):
        # Initial Processing method invoked
        self.initial_processing()
        # Get initial payload to be validated
        payload = self.get_payload()
        # Get validated data from schema
        data = self.get_load_data(data=payload, many=self.patch_many, partial=True)
        # Check for many/single processing and pass instance accordingly
        if self.patch_many:
            instance = None
        else:
            instance = self.get_object()
        # Invoke update method
        resp_data = self.perform_partial_update(instance, data)
        # Return response
        return Response(resp_data, status=self.patch_status_code)

    def perform_update(self, instance, data):
        raise NotImplementedError

    def perform_partial_update(self, instance, data):
        raise NotImplementedError


class DeleteView(APIView):
    """
    View is used to delete one or more records. Subclass is
    supposed to override the perform_delete method and
    handle db processing and return appropriate data
    that is sent out as API Response data
    """
    def delete(self, request, *args, **kwargs):
        # Initial Processing method invoked
        self.initial_processing()
        # Get initial payload to be validated
        payload = self.get_payload()
        # Get validated data from schema
        data = self.get_load_data(data=payload, many=self.delete_many)
        # Check for many/single processing and pass instance accordingly
        if self.delete_many:
            instance = None
        else:
            instance = self.get_object()
        # Invoke delete method
        resp_data = self.perform_delete(instance, data)
        # Return response
        return Response(resp_data, status=status.HTTP_200_OK)

    def perform_delete(self, instance, data):
        raise NotImplementedError

__all__ = ['APIView', 'ListView', 'RetrieveView', 'CreateView', 'UpdateView', 'DeleteView']
