# 10. Adoção de External Secrets em Produção

Data: 2026-02-22

## Status

Aceito

## Contexto

Credenciais em texto plano em manifests Kubernetes elevam risco operacional.

## Decisão

Adotar External Secrets Operator (ESO) como padrão de produção para injeção de segredos em runtime.

## Consequências

### Positivas
- Segredos fora do repositório Git.
- Rotação centralizada por backend de segredos.
- Menor exposição acidental em PRs.

### Negativas
- Dependência de operador adicional no cluster.
- Processo inicial de setup mais complexo.

## Mitigação
- Documentar bootstrap e fallback de emergência.
- Validar presença de `ExternalSecret` em overlays de produção.
