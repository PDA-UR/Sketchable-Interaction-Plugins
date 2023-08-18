import QtQuick
import QtQuick.Controls
import Qt5Compat.GraphicalEffects

Item {
    id: container
    property var texturePointSize: 18

    visible: true

    function updateData(data) {
        if (data.is_overlay_visible !== undefined)
            overlay.visible = data.is_overlay_visible;
        if (data.is_greyed_out) {
            texture.opacity = 0.25;
            filename.opacity = 0.25;
        } else {
            texture.opacity = 1;
            filename.opacity = 1;
        }
        texture.visible = true;
        filename.visible = true;
        filename.color = data.color;
        texture.source = data.img_path;
        filename.text = data.name;
        container.width = data.widget_width;
        texture.width = data.icon_width;
        texture.height = data.icon_height;
        container.height = texture.paintedHeight + filename.paintedHeight + container.texturePointSize;
        texture.anchors.leftMargin = container.width / 2 - texture.width / 2;
        REGION.set_data({
                "container_width": container.width,
                "container_height": container.height
            });
    }

    Text {
        id: edit_filename
        anchors.left: parent.left
        anchors.top: parent.top
        color: "black"
        font.family: "Helvetica"
        font.pointSize: 14
    }
    Image {
        id: texture
        anchors.left: container.left
        anchors.top: container.top
        asynchronous: true
        opacity: 1
        visible: true
    }
    ColorOverlay {
        id: overlay
        anchors.fill: texture
        color: "#88FA842B"
        source: texture
        visible: false
    }
    TextArea {
        id: filename
        anchors.fill: parent
        anchors.top: texture.bottom
        anchors.topMargin: texture.height
        color: "black"
        font.pixelSize: parent.texturePointSize
        horizontalAlignment: TextArea.AlignHCenter
        opacity: 1
        text: "hello world"
        visible: true
        wrapMode: TextEdit.Wrap

        Keys.onPressed: {
            container.height = texture.height + filename.paintedHeight + 18;
        }
        onEditingFinished: REGION.set_data({
                "text": filename.text
            })
    }
}