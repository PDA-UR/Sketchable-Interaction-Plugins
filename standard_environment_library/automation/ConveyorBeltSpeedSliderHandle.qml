import QtQuick 2.7

Item {
  function updateData(data)
  {
    if(data !== undefined)
    {
      container.width = data.containerwidth;
      container.height = data.containerheight;

      if(data.text !== undefined)
        notification.text = data.text;
    }
  }

  id: container
  visible: true

  Rectangle {
    id: rect
    visible: true
    color: "black"

    anchors.fill: parent

    Text {
      id: notification
      visible: true

      anchors.verticalCenter: parent.verticalCenter
      anchors.horizontalCenter: parent.horizontalCenter

      fontSizeMode: Text.Fit
      minimumPixelSize: 14
      font.pixelSize: 14
      color: "white"
      text: "0"
    }

    Text {
      id: notification2
      visible: true

      anchors.horizontalCenter: parent.horizontalCenter
      anchors.top: notification.bottom

      fontSizeMode: Text.Fit
      minimumPixelSize: 12
      font.pixelSize: 12
      color: "white"
      text: "px/s"
    }
  }
}