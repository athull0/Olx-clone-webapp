from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('reg',adduser,name='register'),
    path('login',loginpage,name='login'),
    path('logout',logoutpage,name='logout'),
    path('profile',profilepage,name='profile'),
    path('editpro/<int:eid>',editprofile,name='editpro'),
    path('addpro',addproducts,name='addpro'),
    path('ads',ad_list,name='ads'),
    path('myads/<int:aid>',adedit,name='myads'),
    path('adel/<int:aid>',addelete,name='adel'),
    path('sentmsg/<int:aid>',sentmessage,name='sentmsg'),
    path('inbox',inbox,name='inbox'),
    path('search',search_ads,name='search_ads'),
    path('addetails/<int:aid>',addetailpage,name='addetails'),
    path('allcategory',allcategory),
    path('catdet/<int:cid>',categorylist,name='cat'),
    path('chat/<int:receiver_id>/',chat_page, name='chat_page'),
    path('send-message/',send_message, name='send_message'),
    path('allmessages',allmessages,name='allmessages')
    # path('filter',searchbycategory,name='searchbycategory')

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)