from django.conf.urls import patterns, include, url

import dj_node.nodes.content
import dj_node.nodes.index
import dj_node.nodes.site
import dj_node.users.account
import dj_node.users.password
import dj_node.users.bookmark
import dj_node.users.comment
import dj_node.users.review
import dj_node.users.profile

urlpatterns = patterns('',
    url(r"^$", dj_node.nodes.index.Index.route, name="index"),
    url(r"^/$", dj_node.nodes.index.Index.route, name="index-2"),

    url(r"login/$", dj_node.users.account.LoginNode.route, name="login"),
    url(r"sign-up/$", dj_node.users.account.SignUpNode.route, name="sign-up"),
    url(r"logout/$", dj_node.users.account.Logout.route, name="logout"),

    url(r"password/change/", dj_node.users.password.ChangePasswordNode.route, name="change-password"),
    url(r"password/forgot/", dj_node.users.password. ForgotPasswordNode.route, name="forgot-password"),
    url(r"password/reset/(?P<code>.+)/$", dj_node.users.password.ResetPasswordNode.route, name="reset-password"),

    url(r"profile/$", dj_node.users.profile.MyProfileNode.route, name="my-profile"),
    url(r"profile/(?P<username>.+)/$", dj_node.users.profile.UserProfileNode.route, name="user-profile"),

    url(r"comment/list/", dj_node.users.comment.CommentListNode.route, name="comment-list"),
    url(r"comment/add/", dj_node.users.comment.CommentNode.route, name="comment-add"),

    url(r"review/list/", dj_node.users.review.ReviewListNode.route, name="review-list"),
    url(r"review/add/", dj_node.users.review.ReviewNode.route, name="review-add"),

    url(r"bookmark/list/", dj_node.users.bookmark.BookmarkListNode.route, name="bookmark-list"),
    url(r"bookmark/add/", dj_node.users.bookmark.BookmarkNode.route, name="bookmark-add"),

    url(r"content/list/", dj_node.nodes.content.ContentListNode.route, name="content-list"),
    url(r"content/view/", dj_node.nodes.content.ContentItemNode.route, name="content-item"),

    url(r"site/lock/$", dj_node.nodes.site.SiteLockNode.route, name="site-lock"),
)

