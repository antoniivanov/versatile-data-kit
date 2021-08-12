{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "pipelines-control-service.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "pipelines-control-service.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "pipelines-control-service.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "pipelines-control-service.labels" -}}
helm.sh/chart: {{ include "pipelines-control-service.chart" . }}
{{ include "pipelines-control-service.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{/*
Selector labels
*/}}
{{- define "pipelines-control-service.selectorLabels" -}}
app.kubernetes.io/name: {{ include "pipelines-control-service.fullname" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: {{ include "pipelines-control-service.fullname" . }}-dep
{{- end -}}



{{/*
Create the name of the service account to use
*/}}
{{- define "pipelines-control-service.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
    {{ default (include "pipelines-control-service.fullname" .) .Values.serviceAccount.name }}
{{- else -}}
    {{ default "default" .Values.serviceAccount.name }}
{{- end -}}
{{- end -}}


{{/*
Return the proper Pipelines Control Service image name
*/}}
{{- define "pipelines-control-service.image" -}}
{{- $registryName := .Values.image.registry -}}
{{- $repositoryName := .Values.image.repository -}}
{{- $tag := .Values.image.tag | toString -}}
{{/*
Helm 2.11 supports the assignment of a value to a variable defined in a different scope,
but Helm 2.9 and 2.10 doesn't support it, so we need to implement this if-else logic.
Also, we can't use a single if because lazy evaluation is not an option
*/}}
{{- if .Values.global.imageRegistry }}
    {{- printf "%s/%s:%s" .Values.global.imageRegistry $repositoryName $tag -}}
{{- else -}}
    {{- printf "%s/%s:%s" $registryName $repositoryName $tag -}}
{{- end -}}
{{- end -}}

{{/*
Create the name of the deployment Kubernetes namespace used by Data Jobs
*/}}
{{- define "pipelines-control-service.deploymentK8sNamespace" -}}
{{- if .Values.deploymentK8sNamespace -}}
    {{ .Values.deploymentK8sNamespace }}
{{- else -}}
    {{ .Release.Namespace }}
{{- end -}}
{{- end -}}

{{/*
Create the name of the deployment Kubernetes namespace used by System and builder jobs
*/}}
{{- define "pipelines-control-service.controlK8sNamespace" -}}
{{- if .Values.controlK8sNamespace -}}
    {{ .Values.controlK8sNamespace }}
{{- else -}}
    {{ .Release.Namespace }}
{{- end -}}
{{- end -}}

{{/*
Generate default JDBC credentials for local CockroachDB instance.
*/}}
{{- define "pipelines-control-service.jdbcSecret" -}}
USERNAME: {{ default "root" .Values.database.username | b64enc | quote }}
PASSWORD: {{ default "" .Values.database.password | b64enc | quote }}
JDBC: {{ default (printf "jdbc:postgresql://%s-cockroachdb-public:26257/defaultdb?sslmode=disable" .Release.Name) .Values.database.jdbcUrl | b64enc |quote }}
{{- end -}}

{{/*
JDBC secret name
*/}}
{{- define "pipelines-control-service.jdbcSecretName" -}}
{{ include "common.names.fullname" . }}-jdbc
{{- end -}}