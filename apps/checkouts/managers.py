from __future__ import absolute_import

from django.db import models

from documents.models import Document

from .exceptions import DocumentNotCheckedOut
from .literals import STATE_CHECKED_OUT, STATE_CHECKED_IN


class DocumentCheckoutManager(models.Manager):
    #TODO: 'check_expiration' method
    
    def checked_out_documents(self):
        return Document.objects.filter(pk__in=self.model.objects.all().values_list('pk', flat=True))

    def is_document_checked_out(self, document):
        if self.model.objects.filter(document=document):
            return True
        else:
            return False
            
    def check_in_document(self, document):
        try:
            document_checkout = self.model.objects.get(document=document)
        except self.model.DoesNotExist:
            raise DocumentNotCheckedOut
        else:
            document_checkout.delete()
            
    def document_checkout_info(self, document):
        return self.model.objects.get(document=document)

    def document_checkout_state(self, document):
        if self.is_document_checked_out(document):
            return STATE_CHECKED_OUT
        else:
            return STATE_CHECKED_IN

        
