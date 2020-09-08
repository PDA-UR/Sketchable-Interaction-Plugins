import QtQuick 2.7

Item {
	function updateData(data) {
		texture.width = data.img_width;
		texture.height = data.img_height;
		texture.source = data.img_path;

		texture.anchors.leftMargin = data.widget_width / 2 - texture.width / 2;
		texture.anchors.topMargin = data.widget_height / 2 - texture.height / 2;
	}

	id: container
		visible: true

	Image {
		id: texture
		anchors.left: parent.left
		anchors.top: parent.top

		visible: true
	}

	TextEdit {
        id: te
        width: 240
        horizontalAlignment: TextEdit.AlignHCenter
        verticalAlignment: TextEdit.AlignVCenter
        text: "Hello World"
        font.family: "Helvetica"
        font.pointSize: 20
        color: "black"
        focus: true
        anchors.bottom: texture.top
        anchors.left: texture.left
        anchors.leftMargin: - width / 2
        onTextChanged: REGION.set_data({text: te.text});
    }
}
