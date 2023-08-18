import QtQuick

Item
{
    function updateData(data) {
        container.width = data.width;
        container.height = data.height;
        texture.width = data.img_width;
        texture.height = data.img_height;
        texture.source = data.img_path;

        inbox.text = "Posteingang (" + data.num_unread_emails + "/" + data.num_emails + ")";
    }

    id: container
    visible: true

    Rectangle {
        id: background
        border.width: 1
        border.color: "#F00"
        visible: false
        anchors.fill: parent
    }

    Image {
       id: texture
       anchors.left: parent.left
       anchors.top: parent.top
       anchors.leftMargin: 20
       anchors.topMargin: 20
       visible: true
    }

    Text {
       id: address
       text: "juergen.hahn@ur.de"
       anchors.left: texture.right
       anchors.top: texture.top
       font.family: "Helvetica"
       font.pointSize: 24
       color: "black"
       anchors.leftMargin: 20
       anchors.topMargin: address.height / 4
    }

    Text {
       id: inbox
       text: "Posteingang"
       anchors.left: texture.left
       anchors.top: texture.bottom
       font.family: "Helvetica"
       font.pointSize: 24
       color: "black"
       anchors.topMargin: 10
    }
}