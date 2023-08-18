import QtQuick
import QtQuick.Controls
import Qt5Compat.GraphicalEffects

Item
{
    property var texturePointSize: 18

    function updateData(data)
    {
        if(data.is_overlay_visible !== undefined)
            overlay.visible = data.is_overlay_visible;

        if(data.is_in_preview)
        {
            if(data.is_visible !== undefined)
                container.visible = data.is_visible;

            texture.width = data.icon_width;
            texture.height = data.icon_height;

            if(data.img_path != undefined)
                texture.source = data.img_path;

            container.width = data.container_width
            container.height = data.container_height

            filename.color = data.color;
            filename.text = data.name;
            filename.visible = !data.is_in_preview;

            texture.anchors.leftMargin = 0;
        }
        else
        {
            texture.visible = true;
            filename.visible = true;
            filename.color = data.color;
            texture.source = data.img_path;
            filename.text = data.name;
            container.width = data.widget_width;
            texture.width = data.icon_width;
            texture.height = data.icon_height;
            container.height = texture.height + filename.paintedHeight + container.texturePointSize;
            texture.anchors.leftMargin = container.width / 2 - texture.width / 2;

            if(data.is_greyed_out) {
                texture.opacity = 0.25;
                filename.opacity = 0.25;
            } else {
                texture.opacity = 1;
                filename.opacity = 1;
            }

            REGION.set_data(
            {
                container_width: container.width,
                container_height: container.height,
            });
        }
    }

    id: container

    visible: true

    Image {
        id: texture
        anchors.left: container.left
        anchors.top: container.top
        fillMode: Image.PreserveAspectFit

        visible: true
        cache: true
        asynchronous: true
    }

    ColorOverlay {
        id: overlay
        anchors.fill: texture
        source: texture
        color: "#88FA842B"
        visible: false
    }

    TextArea {
        id: filename
        visible: true
        text: "hello world"
        font.pixelSize: parent.texturePointSize
        color: "black"
        wrapMode: TextEdit.Wrap
        anchors.fill: parent
        anchors.top: texture.bottom
        anchors.topMargin: texture.height
        onEditingFinished: REGION.set_data({text: filename.text});
        horizontalAlignment: TextArea.AlignHCenter

        Keys.onPressed: {
            container.height = texture.height + filename.paintedHeight + 18;
        }
    }
}