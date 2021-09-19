import QtQuick 2.7

Item {
	function updateData(data) {
        container.width = data.width;
        container.height = data.height;

        first_line.text = data.first_line;
        first_line.width = data.width;

        second_line.text = data.second_line;
        second_line.width = data.width;

        third_line.text = data.third_line;
        third_line.width = data.width;

        fourth_line.text = data.fourth_line;
        fourth_line.width = data.width;
	}

	id: container
		visible: true

    Text {
        id: first_line
        visible: true

        font.pixelSize: 72
        color: "white"
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.topMargin: 5
        anchors.leftMargin: 0

        wrapMode: TextEdit.Wrap
        text: "Hello World"
    }

    Text {
        id: second_line
        visible: true

        font.pixelSize: 72
        color: "white"
        anchors.top: first_line.bottom
        anchors.left: parent.left
        anchors.topMargin: 5
        anchors.leftMargin: 0

        wrapMode: TextEdit.Wrap
        text: "Hello World"
    }

    Text {
        id: third_line
        visible: true

        fontSizeMode: Text.Fit
        font.pixelSize: 72
        color: "white"

        anchors.top: second_line.bottom
        anchors.left: parent.left
        anchors.topMargin: 5
        anchors.leftMargin: 0

        wrapMode: TextEdit.Wrap
        text: "Hello World"
    }

    Text {
        id: fourth_line
        visible: true

        fontSizeMode: Text.Fit
        font.pixelSize: 72
        color: "white"
        anchors.top: third_line.bottom
        anchors.left: parent.left
        anchors.topMargin: 5
        anchors.leftMargin: 0

        wrapMode: TextEdit.Wrap
        text: "Hello World"
    }
}
