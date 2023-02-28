import QtQuick 2.7
import QtQuick.Controls 2.7

Item {
    function updateData(data) {
        texture.width = data.img_width;
        texture.height = data.img_height;
        animation.width = data.img_width * 1.5;
        animation.height = data.img_height * 1.5;
        texture.source = data.img_path;
        texture.anchors.leftMargin = data.widget_width / 2 - texture.width / 2;
        texture.anchors.topMargin = data.widget_height / 2 - texture.height / 2;
        animation.anchors.leftMargin = data.widget_width / 2 - animation.width / 2;
        animation.anchors.topMargin = data.widget_height / 2 - animation.height / 2;

        hint.anchors.leftMargin = data.widget_width / 2 - hint.width / 2;

        animation.visible = data.is_loading;
        hint.visible = data.is_loading;
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

    AnimatedImage {
        id: animation
        anchors.left: parent.left
        anchors.top: parent.top
        source: "/home/juergen/1_dev/projects/Sketchable-Interaction/SI/plugins/standard_environment_library/art/res/Loading_icon.gif"
        visible: false
        horizontalAlignment: TextArea.AlignHCenter
    }

    Text {
        id: hint
        anchors.left: parent.left
        anchors.top: animation.bottom
        wrapMode: TextEdit.Wrap
        font.pixelSize: 32
        //anchors.topMargin: -30

        text: "Generating..."
        visible: false
    }
}






