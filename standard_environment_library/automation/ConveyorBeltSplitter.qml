import QtQuick 2.7
import QtQuick.Controls 1.4

Item {
	property string uuid

	function updateData(data) {
		texture.width = data.img_width;
		texture.height = data.img_height;
		texture.source = data.img_path;
		container.uuid = data.uuid;

		texture.anchors.leftMargin = data.widget_width / 2 - texture.width / 2 + 35;
		texture.anchors.topMargin = data.widget_height / 2 - texture.height / 2;

        for(var i = 0; i < data.conditions.length; i++)
            model.append({text: data.conditions[i]});
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

	Text {
            id: output_true
            visible: true

            fontSizeMode: Text.Wrap
            font.pointSize: 15
            color: "black"

            anchors.left: parent.left
            anchors.leftMargin: 35
            anchors.top: parent.top
            anchors.topMargin: 10

            text: "TRUE"
            wrapMode: Text.Wrap
        }

        Text {
            id: output_false
           visible: true

           fontSizeMode: Text.Wrap
           font.pointSize: 15
           color: "black"

           anchors.left: parent.left
           anchors.leftMargin: 28
           anchors.top: parent.top
           anchors.topMargin: 260

           text: "FALSE"
           wrapMode: Text.Wrap
        }

    ComboBox {
        id: cbox
        width: 200
        anchors.top: texture.top
        anchors.left: parent.left
        anchors.leftMargin: 45
        anchors.topMargin: 65
        focus: true

        model: ListModel {
            id: model
            ListElement { text: "<condition>"}
        }

        onCurrentIndexChanged: {
            REGION.set_data({uuid: container.uuid, text: cbox.model.get(currentIndex).text});
        }

        onAccepted: {
            if (find(currentText) === -1) {
                model.append({text: editText})
                currentIndex = find(editText)
            }

            REGION.set_data({uuid: container.uuid, text: cbox.model.get(currentIndex).text});
        }
    }

	//TextInput {
    //    id: te
    //    width: 200
    //    horizontalAlignment: TextEdit.AlignHCenter
    //    verticalAlignment: TextEdit.AlignVCenter
    //    text: "condition"
    //    font.family: "Helvetica"
    //    font.pointSize: 12
    //    color: "black"
    //    focus: true
    //    anchors.top: texture.top
    //    anchors.left: parent.left
    //    anchors.leftMargin: 45
    //    anchors.topMargin: 65
    //    onTextChanged: REGION.set_data({uuid: container.uuid, text: te.text})
    //    onAccepted: REGION.set_data({uuid: container.uuid, text: te.text})
    //}
}
