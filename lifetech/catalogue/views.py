from oscar.apps.catalogue.views import CatalogueView as CoreCatalogueView
from oscar.apps.partner.strategy import Selector
from django.utils.translation import gettext_lazy as _


class CatalogueView(CoreCatalogueView):

    def get_context_data(self, **kwargs):
        ctx = {}
        ctx['summary'] = _("All products")
        search_context = self.search_handler.get_search_context_data(
            self.context_object_name)
        ctx.update(search_context)
        strategy = Selector().strategy()
        available_products = []
        for product in ctx['products']:
            info = strategy.fetch_for_product(product)
            if info.availability.is_available_to_buy:
                available_products.append(product)
        ctx['object_list'] = available_products
        ctx['products'] = available_products
        ctx['paginator'].count = len(available_products)
        return ctx