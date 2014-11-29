attribute vec3 qt_Vertex;
uniform mat4 qt_ModelViewProjectionMatrix;

void main(void)
{
    gl_Position = qt_ModelViewProjectionMatrix * vec4(qt_Vertex, 1.0);
}
