import QtQuick 2.7
import QtQuick.Controls 2.7
import QtGraphicalEffects 1.0

Item
{
    id: container
    function updateData(data)
    {
        if (data.is_highlighted === undefined) {
            overlay.visible = false;
        } else {
            overlay.visible = data.is_highlighted;
        }

        filename.color = data.color;
        texture.source = data.img_path;
        filename.text = data.name;

        var width = data.icon_width;
        if(filename.paintedWidth > width)
            width = filename.paintedWidth;

        var actual_name = "";

        var temp_width = width;
        if (temp_width > data.widget_width) {

            var num_chars = filename.text.length;
            var char_width = width / num_chars;

            var i = 0;
            var num_chars_line = Math.trunc(100 / char_width);
            var num_chars_left = 0;

            for(var i = 0; temp_width > 100; ++i, temp_width -= 100) {
                actual_name += filename.text.substring(i * num_chars_line, (i + 1) * num_chars_line) + "-\n";
                num_chars_left += num_chars_line;
            }

            actual_name += filename.text.substring(num_chars_left);
        } else {
            actual_name = data.name;
        }

        filename.text = actual_name;
        var height = data.icon_height + filename.paintedHeight;
        width = filename.paintedWidth;

        container.width = width + 5;
        container.height = height + 5;

        texture.width = data.icon_width;
        texture.height = data.icon_height;
        texture.anchors.leftMargin = (width - texture.width) / 2 + 2.5;
        texture.anchors.topMargin = 2.5;

        filename.anchors.leftMargin = 2.5;

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

    TextEdit {
        id: filename
        visible: true
        text: ""
        font.pixelSize: 18
        color: "black"
        anchors.verticalCenter: texture.verticalCenter
        textFormat: Text.PlainText
        anchors.top: texture.bottom
        anchors.left: container.left
        wrapMode: Text.Wrap
        focus: true
        onEditingFinished: REGION.set_data({text: filename.text});
    }
}