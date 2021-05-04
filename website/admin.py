from flask import Blueprint, redirect, render_template, flash, url_for
from flask_login import login_required, current_user
from .models import User, Post, Report, Comment
from . import db

admin = Blueprint("admin", __name__)

admins = []

@admin.route('/admin/')
@login_required
def admin_page():
    if len(admins) == 0:
        admins.append('Lucifer')
    if current_user.userName in admins:
        reports = Report.query.all()
        users = User.query.all()
        return render_template('admin.html', reports=reports, admins=admins, users=users)
    else:
        flash('You\'re not an Admin')
        return redirect(url_for('views.home'))

@admin.route('/report-post/<postId>/<url_red>/')
@login_required
def report_post(postId, url_red):
    post = Post.query.filter_by(id=postId).first()
    db.session.add(Report(user=post.userName, ref=postId, desc=f'Post by {post.userName} - {post.desc}', link=f'/post/{ postId }'))
    db.session.commit()
    flash('Post Reported Successfully')
    return redirect(url_for(url_red))

@admin.route('/report-comment/<commentId>/')
@login_required
def report_comment(commentId):
    comment = Comment.query.filter_by(id=commentId).first()
    db.session.add(Report(user=comment.userName, ref=commentId, desc=f'Comment by {comment.userName} - {comment.desc}', link=f'/post/{ comment.postId }'))
    db.session.commit()
    flash('Post Reported Successfully')
    return redirect(url_for('views.post', postId=comment.postId))

@admin.route('/add-admin/<userName>/')
@login_required
def add_admin(userName):
    if current_user.userName in admins:
        admins.append(userName)
    return redirect(url_for('admin.admin_page'))

@admin.route('/remove-admin/<userName>/')
@login_required
def remove_admin(userName):
    if current_user.userName in admins:
        admins.pop(admins.index(userName))
    return redirect(url_for('admin.admin_page'))

@admin.route('/remove-user/<userName>/')
@login_required
def remove_user(userName):
    if current_user.userName in admins:
        user = User.query.filter_by(userName=userName).first()
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('admin.admin_page'))

@admin.route('/take-action/<reportId>/')
@login_required
def take_action(reportId):
    if current_user.userName in admins:
        report = Report.query.filter_by(id=reportId).first()
        if report:
            if 'Post' in report.desc:
                post = Post.query.filter_by(id=report.ref).first()
                db.session.delete(post)
            if 'Comment' in report.desc:
                comment = Comment.query.filter_by(id=report.ref).first()
                post = Post.query.filter_by(id=comment.postId).first()
                post.comments -= 1
                db.session.delete(comment)
            db.session.delete(report)
            db.session.commit()
    return redirect(url_for('admin.admin_page'))