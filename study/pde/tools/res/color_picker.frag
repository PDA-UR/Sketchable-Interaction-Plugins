/*
Taken from https://stackoverflow.com/questions/67394139/get-color-of-element-in-the-point-qml
CC BY-SA 4.0

Original Author: SMR
Original Answer Date: 06.01.2022

Changed to fit for SI Plugin and use with Qt6 QSB by: Jürgen Hahn

Requires compilation with qsb tool.
Command used for current qsb-file color_picker.frag.qsb :: "qsb --glsl 330 -o color_picker.frag.qsb color_picker.frag"
*/
#version 440

layout(location = 0) in vec2 qt_TexCoord0;
layout(location = 0) out vec4 fragColor;

layout(std140, binding = 0) uniform buf {
    mat4 qt_Matrix;
    float qt_Opacity;
    float ringWidth;
    float s;
    float v;
} ubuf;

vec3 hsv2rgb(vec3 c) {
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

void main() {
    vec2 coord = qt_TexCoord0 - vec2(0.5);
    float ring = smoothstep(0.0, 0.01, -abs(length(coord) - 0.5 + ubuf.ringWidth) + ubuf.ringWidth);
    fragColor = vec4(hsv2rgb(vec3(-atan(coord.x, coord.y) / 6.2831 + 0.5, ubuf.s, ubuf.v)), 1.0);
    fragColor *= ring;
}
