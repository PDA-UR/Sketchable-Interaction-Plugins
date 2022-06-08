import QtQuick 2.7
import QtQuick.Controls 2.7
import QtGraphicalEffects 1.0

Item
{
    property var texturePointSize: 18

    id: container
    function updateData(data)
    {
        if(data.icon_view) {
            if(data.is_greyed_out) {
                texture.opacity = 0.25;
                filename.opacity = 0.25;
            } else {
                texture.opacity = 1;
                filename.opacity = 1;
            }

            edit_filename.visible = false;
            edit_textedit.visible = false;
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
                container_height: container.height
            });
        }

        if(data.edit_view) {
            texture.visible = false;
            filename.visible = false;
            edit_filename.visible = true;
            edit_textedit.visible = true;
            edit_filename.text = data.name;
            container.width = data.widget_width;
            container.height = data.widget_height;
            edit_textedit.text = data.content;
        }
    }

    visible: true

    Text {
        id: edit_filename
        anchors.top: parent.top
        anchors.left: parent.left
        font.family: "Helvetica"
        font.pointSize: 14
        color: "black"
    }

    Shortcut {
        sequence: "Ctrl+S"
        onActivated: REGION.set_data({te_content: edit_textedit.text})
    }

    TextEdit {
        id: edit_textedit
        wrapMode: TextEdit.WordWrap
        anchors.top: edit_filename.bottom
        anchors.left: parent.left
        anchors.fill: parent
        anchors.bottom: parent.bottom
        anchors.topMargin: edit_filename.height + 10
        font.pointSize: 12
    }

    Image {
        id: texture
        anchors.left: container.left
        anchors.top: container.top
        asynchronous: true
        opacity: 1

        visible: true
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
        opacity: 1

        Keys.onPressed: {
            container.height = texture.height + filename.paintedHeight + 18;
        }
    }
}