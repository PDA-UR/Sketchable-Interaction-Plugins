import QtQuick

Item
{
    function updateData(data)
    {
        if(data.effect_text !== undefined)
            effect_text.text = data.effect_text;

        if(data.effect_text !== undefined)
            effect_texture.source = data.effect_texture;

        movement_texture.source = data.movement_texture;

        if(effect_text.text === "") {
            effect_text_rect.width = 0;
            effect_text_rect.height = 0;
        } else {
            effect_text_rect.width = effect_text.paintedWidth + 5;
            effect_text_rect.height = effect_text.paintedHeight + 5;
        }

        if(data.visible) {
            if (movement_texture.visible)
                createAnimationMovementTextureOut.start()

            if(!effect_text_rect.visible)
                createAnimationRectIn.start()

            if(!effect_texture.visible)
                createAnimationEffectTextureIn.start()

            if(!effect_text.visible)
                createAnimationTextIn.start()
        } else {
            if (!movement_texture.visible)
                createAnimationMovementTextureIn.start()

            if(effect_text_rect.visible)
                createAnimationRectOut.start()

            if(effect_texture.visible)
                createAnimationEffectTextureOut.start()

            if(effect_text.visible)
                createAnimationTextOut.start()
        }

        if(data.visible !== undefined) {
            effect_text_rect.visible = data.visible;
            effect_text.visible = data.visible;
            effect_texture.visible = data.visible;
            movement_texture.visible = !data.visible;
        }
    }

    id: container

    width: 500
    height: 500

    Image {
        NumberAnimation on opacity {
            id: createAnimationEffectTextureIn
            from: 0
            to: 1
            duration: 350
        }

        NumberAnimation on opacity {
            id: createAnimationEffectTextureOut
            from: 1
            to: 0
            duration: 150
        }

        id: effect_texture
        visible: false
        anchors.left: effect_text_rect.right
        anchors.top: effect_text_rect.top
        width: effect_text.paintedHeight
        height: effect_text.paintedHeight
        anchors.leftMargin: 4
        anchors.topMargin: 2.5
    }

    Image {
        NumberAnimation on opacity {
            id: createAnimationMovementTextureIn
            from: 0
            to: 1
            duration: 350
        }

        NumberAnimation on opacity {
            id: createAnimationMovementTextureOut
            from: 1
            to: 0
            duration: 150
        }

        id: movement_texture
        visible: false
        width: effect_text.paintedHeight
        height: effect_text.paintedHeight
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.leftMargin: 12.5
        anchors.topMargin: 11.5
    }

    Rectangle {
        NumberAnimation on opacity {
            id: createAnimationRectIn
            from: 0
            to: 1
            duration: 350
        }

        NumberAnimation on opacity {
            id: createAnimationRectOut
            from: 1
            to: 0
            duration: 150
        }

        visible: false
        id: effect_text_rect
        width: 0
        height: 0
        color: "white"
        border.color: "black"
        border.width: 1
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.leftMargin: 12.5
        anchors.topMargin: 11.5
    }

    Text {
        NumberAnimation on opacity {
            id: createAnimationTextIn
            from: 0
            to: 1
            duration: 350
        }

        NumberAnimation on opacity {
            id: createAnimationTextOut
            from: 1
            to: 0
            duration: 150
        }

        id: effect_text
        visible: true
        color: "black"
        text: ""
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.leftMargin: 15
        anchors.topMargin: 14
        font.bold: true
    }
}