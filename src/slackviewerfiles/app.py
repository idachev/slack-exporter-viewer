import flask

from slackviewerfiles.utils.slack_utils import slack_build_thumb, slack_check_download

app = flask.Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)


def get_sorted_data():
    channels = list(flask._app_ctx_stack.channels.keys())
    groups = list(flask._app_ctx_stack.groups.keys())
    dm_users = list(flask._app_ctx_stack.dm_users)
    mpim_users = list(flask._app_ctx_stack.mpim_users)

    channels.sort(key=lambda k: k.lower())
    groups.sort(key=lambda k: k.lower())
    dm_users.sort(key=lambda k: k['users'][0].display_name.lower())
    mpim_users.sort(key=lambda k: k['name'].lower())

    return channels, groups, dm_users, mpim_users


@app.route("/channel/<name>/")
def channel_name(name):
    messages = flask._app_ctx_stack.channels[name]

    channels, groups, dm_users, mpim_users = get_sorted_data()

    return flask.render_template("viewer.html", messages=messages,
                                 name=name.format(name=name),
                                 channels=sorted(channels),
                                 groups=sorted(groups) if groups else {},
                                 dm_users=dm_users,
                                 mpim_users=mpim_users,
                                 no_sidebar=app.no_sidebar,
                                 no_external_references=app.no_external_references)


@app.route("/group/<name>/")
def group_name(name):
    messages = flask._app_ctx_stack.groups[name]

    channels, groups, dm_users, mpim_users = get_sorted_data()

    return flask.render_template("viewer.html", messages=messages,
                                 name=name.format(name=name),
                                 channels=sorted(channels),
                                 groups=sorted(groups),
                                 dm_users=dm_users,
                                 mpim_users=mpim_users,
                                 no_sidebar=app.no_sidebar,
                                 no_external_references=app.no_external_references)


@app.route("/dm/<id>/")
def dm_id(id):
    messages = flask._app_ctx_stack.dms[id]

    channels, groups, dm_users, mpim_users = get_sorted_data()

    return flask.render_template("viewer.html", messages=messages,
                                 id=id.format(id=id),
                                 channels=sorted(channels),
                                 groups=sorted(groups),
                                 dm_users=dm_users,
                                 mpim_users=mpim_users,
                                 no_sidebar=app.no_sidebar,
                                 no_external_references=app.no_external_references)


@app.route("/mpim/<name>/")
def mpim_name(name):
    messages = flask._app_ctx_stack.mpims[name]

    channels, groups, dm_users, mpim_users = get_sorted_data()

    return flask.render_template("viewer.html", messages=messages,
                                 name=name.format(name=name),
                                 channels=sorted(channels),
                                 groups=sorted(groups),
                                 dm_users=dm_users,
                                 mpim_users=mpim_users,
                                 no_sidebar=app.no_sidebar,
                                 no_external_references=app.no_external_references)


@app.route('/files.slack.com/<path:path>')
def send_files_slack_com(path):
    f_path = 'files.slack.com/' + path

    slack_build_thumb(flask._app_ctx_stack.files_path, f_path)

    f_path = slack_check_download(flask._app_ctx_stack.files_path, f_path)

    return flask.send_from_directory(flask._app_ctx_stack.files_path, f_path)


@app.route('/avatars.slack-edge.com/<path:path>')
def send_avatars_slack_edge_com(path):
    return flask.send_from_directory(flask._app_ctx_stack.files_path,
                                     'avatars.slack-edge.com/' + path)


@app.route("/")
def index():
    channels, groups, dm_users, mpim_users = get_sorted_data()

    if channels:
        if "general" in channels:
            return channel_name("general")
        else:
            return channel_name(channels[0])
    elif groups:
        return group_name(groups[0])
    elif dms:
        return dm_id(dms[0])
    elif mpims:
        return mpim_name(mpims[0])
    else:
        return "No content was found in your export that we could render."
