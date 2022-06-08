import QtQuick 2.7
import QtQuick.Controls 2.7

Item
{
    function updateData(data)
    {
        if(data.item_view) {
            container.width = data.widget_width;
            container.height = data.widget_height;
            if (data.is_unread)
                unread_marker_item.visible = true;
            else
                unread_marker_item.visible = false;
            email_sender_fixed.visible = true;
            email_sender.visible = true;
            email_receiver_fixed.visible = true;
            email_receiver.visible = true;
            email_subject_fixed.visible = true;
            email_subject.visible = true;

            email_subject.text = data.email_subject;
            email_sender.text = data.email_sender;
            email_receiver.text = data.email_sender;

            date.visible = true;
            date.text = data.date;
            texture.visible = false;
            icon_email_sender.visible = false;
            icon_email_subject.visible = false;

            texture_read_view.visible = false;
            sender_read_view.visible = false;
            receiver_read_view.visible = false;
            subject_read_view.visible = false;
            message_read_view.visible = false;
            unread_marker_icon.visible = false;
            date_read_view.visible = false;
        }

        if(data.icon_view) {
            container.width = data.widget_width;
            container.height = data.widget_height;
            unread_marker_item.visible = false;
            email_sender_fixed.visible = false;
            email_sender.visible = false;
            email_receiver_fixed.visible = false;
            email_receiver.visible = false;
            email_subject_fixed.visible = false;
            email_subject.visible = false;
            date.visible = false;
            texture.visible = true;
            icon_email_sender.visible = true;
            icon_email_subject.visible = true;

            icon_email_sender.text = data.email_sender;
            icon_email_subject.text = data.email_subject;

            texture.source = data.img_path;
            texture.width = data.icon_width;
            texture.height = data.icon_height;

            texture_read_view.visible = false;
            sender_read_view.visible = false;
            receiver_read_view.visible = false;
            subject_read_view.visible = false;
            message_read_view.visible = false;
            unread_marker_icon.visible = true;
            date_read_view.visible = false;

            if (data.is_unread)
                unread_marker_icon.visible = true;
            else
                unread_marker_icon.visible = false;
        }

        if(data.read_view) {
            container.width = data.widget_width;
            container.height = data.widget_height;
            unread_marker_item.visible = false;
            unread_marker_icon.visible = false;
            email_sender_fixed.visible = false;
            email_sender.visible = false;
            email_receiver_fixed.visible = false;
            email_receiver.visible = false;
            email_subject_fixed.visible = false;
            email_subject.visible = false;
            date.visible = false;
            texture.visible = false;
            icon_email_sender.visible = false;
            icon_email_subject.visible = false;
            unread_marker_icon.visible = false;

            texture_read_view.visible = true;
            sender_read_view.visible = true;
            receiver_read_view.visible = true;
            subject_read_view.visible = true;
            message_read_view.visible = true;
            date_read_view.visible = true;
            date_read_view.text = data.date;

            sender_read_view.text = data.email_sender;
            receiver_read_view.text = data.email_receiver;
            subject_read_view.text = data.email_subject;
            message_read_view.text = data.email_message;

            texture_read_view.source = data.img_path;
            texture_read_view.width = data.icon_width;
            texture_read_view.height = data.icon_height;
        }
    }

    id: container
    visible: true

    Text {
        id: date_read_view
        width: parent.width
        text: Qt.formatDateTime(new Date(), "dd.MM.yyyy, hh:mm:ss")
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.leftMargin: 220
        visible: false
    }

    Rectangle {
        id: unread_marker_icon
        width: (parent.width < parent.height ? parent.width : parent.height) / 4
        height: width
        color: "#0078D7"
        radius: width * 0.5
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.topMargin: 15
        anchors.leftMargin: 25
    }

    Image {
        id: texture_read_view
        visible: false
        anchors.left: parent.left
        anchors.top: parent.top
        asynchronous: true
    }

    Text {
        id: sender_read_view
        visible: false
        text: "Von: Raphael Wimmer <raphael.wimmer@ur.de>"
        anchors.left: texture_read_view.right
        anchors.top: texture_read_view.top
        anchors.topMargin: 20
        anchors.leftMargin: 5
    }

    Text {
        id: receiver_read_view
        visible: false
        text: "An: Mich <juergen.hahn@ur.de>"
        anchors.left: texture_read_view.right
        anchors.top: sender_read_view.bottom
        anchors.leftMargin: 5
    }

    Text {
        id: subject_read_view
        visible: false
        text: "Betreff: DEMO FÜR DEN MP FERTIGMACHEN!"
        anchors.top: texture_read_view.bottom
        font.family: "Helvetica"
        font.pointSize: 12
        color: "black"
        font.bold: true
        anchors.leftMargin: 5
    }

    TextArea {
        id: message_read_view
        visible: false
        text: "Do you see any Teletubbies in here? Do you see a slender plastic tag clipped to my shirt with my name printed on it? Do you see a little Asian child with a blank expression on his face sitting outside on a mechanical helicopter that shakes when you put quarters in it? No? Well, that's what you see at a toy store. And you must think you're in a toy store, because you're here shopping for an infant named Jeb."
        anchors.top: subject_read_view.bottom
        anchors.bottom: parent.bottom
        anchors.topMargin: 110
        wrapMode: TextEdit.WordWrap
        anchors.fill: parent
        font.pointSize: 12
    }

    Image {
        id: texture
        anchors.left: parent.left
        anchors.top: parent.top
        asynchronous: true

        visible: false
    }

    Text {
        id: icon_email_sender
        width: parent.width
        anchors.top: texture.bottom
        text: "Raphael Wimmer"
        font.family: "Helvetica"
        font.pointSize: 10
        color: "black"
        visible: false
    }

    Text {
        id: icon_email_subject
        width: parent.width
        anchors.top: icon_email_sender.bottom
        text: "Raphael Wimmer"
        font.family: "Helvetica"
        font.pointSize: 10
        color: "black"
        visible: false
    }


    Rectangle {
        id: unread_marker_item
        width: (parent.width < parent.height ? parent.width : parent.height) / 4
        height: width
        color: "#0078D7"
        radius: width * 0.5
        anchors.left: parent.left
        anchors.verticalCenter: parent.verticalCenter
        anchors.leftMargin: 10
    }

    Text {
        id: email_sender_fixed
        width: parent.width
        text: "Von:"
        anchors.left: unread_marker_item.right
        anchors.leftMargin: 10
        anchors.top: parent.top
        font.family: "Helvetica"
        font.pointSize: 10
        color: "black"
    }

    Text {
        id: email_sender
        width: parent.width
        text: "Raphael Wimmer <raphael.wimmer@ur.de>"
        anchors.left: parent.left
        anchors.leftMargin: 100
        anchors.top: email_sender_fixed.top
        font.family: "Helvetica"
        font.pointSize: 10
        color: "black"
    }

    Text {
        id: email_receiver_fixed
        width: parent.width
        text: "An:"
        anchors.left: unread_marker_item.right
        anchors.leftMargin: 10
        anchors.top: email_sender.bottom
        font.family: "Helvetica"
        font.pointSize: 10
        color: "black"
    }

    Text {
        id: email_receiver
        width: parent.width
        text: "Mich <juergen.hahn@ur.de>"
        anchors.left: parent.left
        anchors.leftMargin: 100
        anchors.top: email_receiver_fixed.top
        font.family: "Helvetica"
        font.pointSize: 10
        color: "black"
    }

    Text {
        id: email_subject_fixed
        width: parent.width
        text: "Betreff:"
        anchors.left: unread_marker_item.right
        anchors.leftMargin: 10
        anchors.bottom: parent.bottom
        font.family: "Helvetica"
        font.pointSize: 14
        color: "black"
        font.bold: true
    }

    Text {
        id: email_subject
        width: parent.width
        text: "BITTE DEMO FÜR MP FERTIG MACHEN"
        anchors.left: parent.left
        anchors.leftMargin: 140
        anchors.bottom: parent.bottom
        font.family: "Helvetica"
        font.pointSize: 14
        color: "black"
        font.bold: true
    }

    Text {
        id: date
        width: parent.width
        text: Qt.formatDateTime(new Date(), "dd.MM.yyyy, hh:mm:ss")
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.leftMargin: 400
        font.family: "Helvetica"
        font.pointSize: 12
        color: "black"
    }
}