import QtQuick 2.7
import QtQuick.Controls 1.4

Item {
    function updateData(data) {
        texture.width = data.img_width;
        texture.height = data.img_height;
        texture.source = data.img_path;
        texture.anchors.leftMargin = data.widget_width / 2 - texture.width / 2;
        texture.anchors.topMargin = data.widget_height / 2 - texture.height / 2;

        if(data.contact !== undefined)
            contact.text = data.contact;
    }

    id: container
    visible: true
    Image {
        id: texture
        anchors.left: parent.left
        anchors.top: parent.top
        asynchronous: true

        visible: true
    }

    Text {
        id: to_contact
        text: "To: "
        anchors.top: texture.bottom
        anchors.left: texture.left
        anchors.leftMargin: texture.width / 2 + container.width / 2 - (to_contact.width / 2 + contact.width / 2)
    }

    Text {
        id: contact
        text: ""
        anchors.left: to_contact.right
        anchors.top: to_contact.top
    }
}

