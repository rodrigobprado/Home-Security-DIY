# Product Requirements Document (PRD) - Módulo de Defesa Não Letal

**Data:** 2026-02-17
**Status:** Draft
**Autor:** Home Security DIY Agent

---

## 1. Introdução

Este módulo descreve o sistema de defesa ativa não letal para os drones (UGV e UAV) do projeto Home Security DIY. O objetivo é fornecer capacidades de **dissuasão** (deterrence) e **intervenção leve** para proteger a propriedade, respeitando estritamente a legislação local e princípios éticos.

**PRINCÍPIO FUNDAMENTAL:** NENHUMA AÇÃO DE DEFESA ATIVA PODE SER AUTOMATIZADA. A decisão de disparo (som, luz, ou spray) deve ser **exclusivamente humana** (Human-in-the-Loop), autenticada e auditável.

## 2. Requisitos Funcionais

### 2.1 Níveis de Resposta

O sistema opera em escalas de escalada de força (Force Continuum):

1.  **Nível 0 - Presença (Passivo/Autônomo):** O drone se posiciona visivelmente e acompanha o alvo.
2.  **Nível 1 - Advertência Visual (Passivo/Autônomo):** Strobes de alta intensidade e holofotes apontados para o alvo.
3.  **Nível 2 - Advertência Sonora (Passivo/Autônomo):** Reprodução de mensagens pré-gravadas ("Atenção, propriedade privada, a polícia foi acionada") e sirene.
4.  **Nível 3 - Intervenção Ativa (Ativo/Manual):** Disparo de agente dissuasor (Spray de Pimenta/Água/Tinta ou Dispersão de Gás CO2 - conforme legalidade). **Requer Autenticação Dupla.**

### 2.2 Protocolo de Segurança (Safety)

*   **P-01 (Human-in-the-Loop):** O gatilho do Nível 3 é bloqueado por software e hardware.
*   **P-02 (Two-Man Rule / 2FA):** Para armar o sistema de Nível 3, o operador deve confirmar via App E inserir um código PIN/Biometria.
*   **P-03 (Geofencing):** O sistema de defesa é desabilitado automaticamente fora do perímetro da propriedade.
*   **P-04 (Timeout):** O sistema se desarma automaticamente após 60 segundos se não houver disparo.

### 2.3 Auditoria

*   Todos os eventos de armação e disparo são registrados em log imutável (Black Box) local e remoto (Home Assistant).
*   Gravação de vídeo é forçada ("Always On") durante qualquer evento de defesa.

## 3. Requisitos Técnicos

### 3.1 Hardware

*   **Áudio:** Módulo Amplificador Classe D (PAM8403) + Alto-falante Sirene (110dB).
*   **Visual:** LED Power Strobe (3W-10W) controlado por MOSFET.
*   **Atuador (Nível 3):** Solenoide 12V ou Servo Motor para acionamento mecânico de válvula/spray.
*   **Segurança Hardware:** Chave física (Relé) que corta a alimentação do Atuador (Nível 3) a menos que o "Arming" esteja ativo.

### 3.2 Software

*   **Módulo de Controle (Python/ROS2):**
    *   Tópico `defense/status`: `idle` | `armed` | `active`
    *   Tópico `defense/command`: `arm` | `disarm` | `trigger`
*   **Integração Home Assistant:**
    *   Card de Defesa com teclado numérico para PIN.
    *   Notificação crítica "Solicitação de Intervenção".

## 4. Análise Legal e Ética

*   **Legítima Defesa:** O uso deve ser proporcional à ameaça.
*   **Responsabilidade:** O operador humano é 100% responsável pelo acionamento. O sistema apenas executa.
*   **Falhas:** Em caso de perda de sinal, o sistema **desarma** imediatamente (Fail-Safe), ao contrário de drones militares que podem ter regras de engajamento diferentes.

## 5. Implementação MVP

Para a primeira versão (v1.0), focaremos nos Níveis 0, 1 e 2 (Visual/Sonoro). O Nível 3 será apenas "Logic-Ready" (software pronto, hardware simulado) para evitar riscos durante o desenvolvimento.

---
