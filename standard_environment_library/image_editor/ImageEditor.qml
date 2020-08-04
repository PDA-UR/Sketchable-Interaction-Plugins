import QtQuick 2.7

Item {
	function updateData(data) {
		texture.width = data.img_width;
		texture.height = data.img_height;
		texture.source = data.img_path;

		texture.anchors.leftMargin = data.widget_width / 2 - texture.width / 2;
		texture.anchors.topMargin = data.widget_height / 2 - texture.height / 2;

        container.width = data.container_width;
        container.height = data.container_height;

        filename.text = data.name;
        filename.width = container.width;
	}

	id: container
		visible: true

    Text {
        id: filename
        visible: true

        width: 400
        fontSizeMode: Text.Fit
        minimumPixelSize: 16
        font.pixelSize: 72
        color: "white"
        anchors.top: parent.top
        anchors.left: parent.left

        wrapMode: TextEdit.Wrap
    }

	Image {
		id: texture
		anchors.left: parent.left
		anchors.top: parent.top

		visible: true
	}
}
