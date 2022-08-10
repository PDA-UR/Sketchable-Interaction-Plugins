import QtQuick 2.7
import QtQuick.Controls 2.7
import QtGraphicalEffects 1.0

Item
{
    id: container
    property var texturePointSize: 18

    function updateData(data)
    {
        if (data.is_highlighted === undefined) {
            overlay.visible = false;
        } else {
            overlay.visible = data.is_highlighted;
        }

        if(data.is_greyed_out) {
            texture.opacity = 0.25;
            filename.opacity = 0.25;
        } else {
            texture.opacity = 1;
            filename.opacity = 1;
        }

        if(data.search_hit_count !== undefined) {
            search_hit_count.text = data.search_hit_count
            search_hit_count.visible = data.search_hit_count_visible
            search_hit_count_fixed.visible = data.search_hit_count_visible
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

        REGION.set_data(
        {
            container_width: container.width,
            container_height: container.height,
        });
    }

    visible: true

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
        source: texture
        color: "#880078D7"
        visible: false
    }

    Text {
        id: search_hit_count
        visible: false
        text: "1"
        color: "white"
        font.family: "Helvetica"
        font.pointSize: 20
        anchors.left: texture.left
        anchors.top: texture.top
        anchors.right: texture.right
        horizontalAlignment: Text.AlignHCenter
    }

    Text {
        id: search_hit_count_fixed
        visible: false
        text: "found"
        color: "white"
        font.family: "Helvetica"
        font.pointSize: 12
        anchors.left: texture.left
        anchors.top: search_hit_count.bottom
        anchors.bottom: texture.bottom
        anchors.right: texture.right
        anchors.leftMargin: 5
    }

    TextArea {
        id: filename
        visible: true
        text: "hello world"
        font.pixelSize: parent.texturePointSize
        color: "black"
        wrapMode: TextEdit.Wrap
        horizontalAlignment: TextArea.AlignHCenter
        anchors.fill: parent
        anchors.top: texture.bottom
        anchors.topMargin: texture.height
        onEditingFinished: REGION.set_data({text: filename.text});

        Keys.onReturnPressed: {
            focus = false;
            editingFinished();
        }

        Keys.onPressed: {
            container.height = texture.height + filename.paintedHeight + 18;
        }
    }
}