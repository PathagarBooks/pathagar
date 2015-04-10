# Copyright (C) 2010, One Laptop Per Child
# Copyright (C) 2010, Kushal Das
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from django.conf import settings

# Number of books shown per page in the OPDS catalogs and in the HTML
# pages:

BOOKS_PER_PAGE = getattr(settings, 'BOOKS_PER_PAGE', 2) 

# If True, serve static media via Django.  Note that this is not
# recommended for production:

BOOKS_STATICS_VIA_DJANGO = getattr(settings, 'BOOKS_STATICS_VIA_DJANGO', False)

# This needs to match the published status

BOOK_PUBLISHED = getattr(settings, 'BOOK_PUBLISHED', 1)

# Features

ALLOW_USER_COMMENTS = False
