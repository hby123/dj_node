from django.conf.urls import patterns, include, url

import dj_node.nodes.index
import dj_node.nodes.site
import dj_node.users.account
import dj_node.nodes.user_content
import dj_node.users.password
import dj_node.users.bookmark
import dj_node.users.comment
import dj_node.users.review
import dj_node.users.profile

#import users.mailing_list

urlpatterns = patterns('',
                       url(r"^$", dj_node.nodes.index.Index.route),
                       url(r"^/$", dj_node.nodes.index.Index.route),
                       url(r"^mojo/$", dj_node.nodes.index.Index.route),

                       url(r"login/$", dj_node.users.account.LoginNode.route),
                       url(r"signup/$", dj_node.users.account.SignUpNode.route),
                       url(r"logout/$", dj_node.users.account.Logout.route),

                       url(r"password/change/", dj_node.users.password.ChangePasswordNode.route),
                       url(r"password/forgot/", dj_node.users.password. ForgotPasswordNode.route),
                       url(r"password/reset/", dj_node.users.password.ResetPasswordNode.route),

                       url(r"profile/bookmarks", dj_node.users.bookmark.BookmarkNode.route),
                       url(r"profile/(?P<username>.+)/$", dj_node.users.profile.ProfileNode.route),
                       url(r"profile/$", dj_node.users.profile.ProfileNode.route),

                       url(r"comment/list/", dj_node.users.comment.CommentListNode.route),
                       url(r"comment/add/", dj_node.users.comment.CommentNode.route),

                       url(r"review/list/", dj_node.users.review.ReviewListNode.route),
                       url(r"review/add/", dj_node.users.review.ReviewNode.route),

                       url(r"bookmark/list/", dj_node.users.bookmark.BookmarkListNode.route),
                       url(r"bookmark/add/", dj_node.users.bookmark.BookmarkNode.route),

                       #url(r"bookmark/delete/",  users.bookmark.BookmarkRemoveForm.route),

    #url(r"mailing-list/add/", users.mailing_list.MailingListForm.route),
    url(r"site/lock/$", dj_node.nodes.site.SiteLockNode.route)

                       )

