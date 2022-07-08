import QtQuick 2.7
import QtQuick.Controls 2.7

Item {
    property var texturePointSize: 18
    property var initial_height: container.height

    function updateData(data) {
        filename.visible = true;
        filename.text = data.name;
        container.width = data.widget_width;

        if(data.is_greyed_out) {
            filename.opacity = 0.25;
        } else {
            filename.opacity = 1;
        }

        container.height = data.height + filename.paintedHeight + container.texturePointSize;
        container.initial_height = data.height;

        REGION.set_data(
        {
            container_width: container.width,
            container_height: container.height,
        });
    }

    id: container
    visible: true
    Image {
        id: texture
        anchors.left: container.left
        anchors.top: container.top
        asynchronous: true

        visible: true
    }

    TextArea {
        id: filename
        width: container.width
        visible: true
        text: "hello world"
        font.pixelSize: parent.texturePointSize
        color: "black"
        anchors.bottom: container.bottom;
        anchors.horizontalCenter: container.horizontalCenter;
        wrapMode: TextEdit.Wrap
        onEditingFinished: REGION.set_data({text: filename.text});
        horizontalAlignment: TextArea.AlignHCenter

        Keys.onPressed: {
            container.height = container.initial_height + filename.paintedHeight + container.texturePointSize;
        }
    }
}