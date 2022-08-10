import QtQuick 2.7

Item {
	function updateData(data) {
		texture.width = data.widget_height;
        texture.height = data.widget_height;
        texture.source = data.img_path;
        container.width = data.widget_width;
        container.height = data.widget_height;
	}

	id: container

	Image {
		id: texture
		anchors.left: parent.left
		anchors.top: parent.top
        asynchronous: true

		visible: true
	}

	Rectangle {
        id: bg
        color: "white"
        anchors.top: parent.top
        anchors.left: texture.right
        width: parent.width
        height: parent.height
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.topMargin: 5
        anchors.bottomMargin: 5
        anchors.leftMargin: 5
        anchors.rightMargin: 5
        border.color: "black"
        border.width: 1
        visible: true
    }

	TextEdit {
        id: te
        text: "TEST"
        font.family: "Helvetica"
        font.pointSize: 20
        color: "black"
        focus: true
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.left: texture.right
        anchors.topMargin: 5
        anchors.bottomMargin: 5
        anchors.leftMargin: 5
        anchors.rightMargin: 5
        onTextChanged: REGION.set_data({text: te.text});

        Keys.onReturnPressed: {
            textChanged();
        }

        Keys.onPressed: {
        }
    }
}
