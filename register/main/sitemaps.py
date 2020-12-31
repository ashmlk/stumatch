from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"

    def items(self):
        return ["main:user_login", "main:site-about", "main:contact-us"]

    def location(self, item):
        return reverse(item)
