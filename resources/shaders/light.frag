uniform mediump vec4 color;

varying float lightIntensity;

void main(void)
{
    gl_FragColor = color * lightIntensity;
}
