import QtQuick 2.7

Item {
    function updateData(data) {
        filename.visible = true;
        filename.text = data.name;
        container.width = data.widget_width;

        if(filename.contentWidth > data.widget_width)
        {
            var actual_name = "";

            var diff = filename.contentWidth - data.widget_width;
            var num_chars = filename.text.length;
            var char_width = filename.contentWidth / num_chars;

            var chars_per_line = Math.trunc(data.widget_width / char_width);
            var lines = Math.trunc(num_chars / chars_per_line) + 1;

            for(var i = 0; i < lines; ++i)
                actual_name += filename.text.substring(i * chars_per_line, (i + 1) * chars_per_line) + "-\n";

            actual_name = actual_name.substring(0, actual_name.length - 2);
            filename.text = actual_name;

            container.width = filename.paintedWidth;
        } else {
            container.width = data.widget_width;
        }

        container.height = data.height + filename.paintedHeight;
        filename.anchors.bottom = container.bottom;
        filename.anchors.horizontalCenter = container.horizontalCenter;

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

    TextEdit {
        id: filename
        visible: true
        text: ""
        font.pixelSize: 18
        color: "black"
        textFormat: Text.PlainText
        wrapMode: Text.Wrap
        focus: true
        onEditingFinished: REGION.set_data({text: filename.text});
    }
}