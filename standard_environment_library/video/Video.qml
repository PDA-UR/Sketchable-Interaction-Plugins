import QtQuick 2.7
import QtMultimedia 5.14
import siqml 1.0

Item
{
    function updateData(data)
    {
        if(data.image)
        {
            container.width = data.widget_width;
            container.height = data.widget_height;
            video.onVideoFrameReady(data.image);
            video_texture.width = data.img_width;
            video_texture.height = data.img_height;
            video_texture.anchors.leftMargin = data.widget_width / 2 - video_texture.width / 2;
            video_texture.anchors.topMargin = data.widget_height / 2 - video_texture.height / 2;
        }

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

    VideoItem {
        id: video
    }

    VideoOutput {
        id: "video_texture";
        fillMode: VideoOutput.PreserveAspectCrop;
        source: video;
        visible: true;
    }
}