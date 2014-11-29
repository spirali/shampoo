/* Const */
const float SpecularContribution = 0.3;
const float DiffuseContribution  = 0.4;

/* In */
attribute vec3 qt_Vertex;
attribute vec3 qt_Normal;


/* Uniform */
uniform mat4 qt_ModelViewProjectionMatrix;
uniform mat3 qt_NormalMatrix;
uniform vec3 lightPosition;

/* Out */
varying float lightIntensity;

void main(void)
{
    gl_Position = qt_ModelViewProjectionMatrix * vec4(qt_Vertex, 1.0);
    vec3 tnorm = normalize(qt_NormalMatrix * qt_Normal);
    vec3 lightVec  = normalize(lightPosition - vec3(gl_Position));
    vec3 reflectVec = reflect(-lightVec, tnorm);
    vec3 viewVec = normalize(-vec3(gl_Position));
    float diffuse = abs(dot(lightVec, tnorm));
    /* Correct way is to compute diffuse like:
       float diffuse = max(dot(lightVec, tnorm), 0.0);
       But models have sometimes invalid normals and we want to see something
    */
    float spec      = 0.0;
    if (diffuse > 0.0) {
        spec = max(dot(reflectVec, viewVec), 0.0);
        spec = pow(spec, 32.0);
    }
    lightIntensity = DiffuseContribution * diffuse +
                     SpecularContribution * spec + 0.4;
}
