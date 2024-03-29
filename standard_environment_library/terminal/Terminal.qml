import QtQuick 2.7
import QtQuick.Controls 2.7

Item {
	function updateData(data) {
		texture.width = data.img_width;
		texture.height = data.img_height;
		texture.source = data.img_path;
		texture.anchors.leftMargin = data.widget_width / 2 - texture.width / 2;
		texture.anchors.topMargin = data.widget_height / 2 - texture.height / 2;

        if(data.visible !== undefined)
            texture.visible = data.visible;

        container.width = data.width;
        container.height = data.height;

        content.append(data.message);
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

    ScrollView {
        id: scroll_view
        width: parent.width
        height: parent.height

        TextArea {
            width: parent.width
            height: parent.height
            id: content
            font.pixelSize: 14
            text: ""
            wrapMode: TextEdit.Wrap
        }
    }
}
