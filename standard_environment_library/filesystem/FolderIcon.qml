import QtQuick
import QtQuick.Controls
import Qt5Compat.GraphicalEffects

Item {
    id: container
    property var texturePointSize: 18

    visible: true

    function updateData(data) {
        if (data.is_highlighted === undefined) {
            overlay.visible = false;
        } else {
            overlay.visible = data.is_highlighted;
        }
        if (data.is_greyed_out) {
            texture.opacity = 0.25;
            filename.opacity = 0.25;
        } else {
            texture.opacity = 1;
            filename.opacity = 1;
        }
        if (data.search_hit_count !== undefined) {
            search_hit_count.text = data.search_hit_count;
            search_hit_count.visible = data.search_hit_count_visible;
            search_hit_count_fixed.visible = data.search_hit_count_visible;
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

    Image {
        id: texture
        anchors.left: container.left
        anchors.top: container.top
        asynchronous: true
        visible: true
    }
    ColorOverlay {
        id: overlay
        anchors.fill: texture
        color: "#880078D7"
        source: texture
        visible: false
    }
    Text {
        id: search_hit_count
        anchors.left: texture.left
        anchors.right: texture.right
        anchors.top: texture.top
        color: "white"
        font.family: "Helvetica"
        font.pointSize: 20
        horizontalAlignment: Text.AlignHCenter
        text: "1"
        visible: false
    }
    Text {
        id: search_hit_count_fixed
        anchors.bottom: texture.bottom
        anchors.left: texture.left
        anchors.leftMargin: 5
        anchors.right: texture.right
        anchors.top: search_hit_count.bottom
        color: "white"
        font.family: "Helvetica"
        font.pointSize: 12
        text: "found"
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
        text: "hello world"
        visible: true
        wrapMode: TextEdit.Wrap

        Keys.onPressed: {
            container.height = texture.height + filename.paintedHeight + 18;
        }
        Keys.onReturnPressed: {
            focus = false;
            editingFinished();
        }
        onEditingFinished: REGION.set_data({
                "text": filename.text
            })
    }
}