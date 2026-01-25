{{- define "ai-native.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "ai-native.fullname" -}}
{{- printf "%s-%s" .Release.Name (include "ai-native.name" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}
