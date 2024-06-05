import streamlit as st

def perguntas_page():
    try:
        perguntas = st.session_state['PERGUNTAS']
        
        if 'indice_pergunta' not in st.session_state:
            st.session_state['indice_pergunta'] = 0

            st.title('Quiz - Teste seus conhecimentos')
            pergunta_atual = perguntas[st.session_state['indice_pergunta']]
            st.subheader(f'Pergunta: {pergunta_atual}')
        
        if st.session_state['indice_pergunta']>0:
            st.title('Quiz - Teste seus conhecimentos')
            pergunta_atual = perguntas[st.session_state['indice_pergunta']]
            st.subheader(f'Pergunta: {pergunta_atual}')
        
        # Permite que o usuário insira sua resposta
        resposta_usuario = st.text_input(f'Resposta para a pergunta {st.session_state["indice_pergunta"] + 1}:')
        
        if resposta_usuario!='':
            ia = st.session_state['CHAT'].pergunta_pdf_with_context([{'role': 'assistant', 'content': "Pergunta:"+perguntas[st.session_state['indice_pergunta']]},{'role': 'user', 'content': "Resposta:"+resposta_usuario+"\n\n\n Você é um professor rigoroso e tem que dar uma nota de 0 a 10 para essa resposta.Qual nota daria? Qual motivo? Qual a resposta correta? Escreva da seguinte forma: Nota: XX \n\n Motivo: XXX \n\n Resposta Correta: XXX"}])
            st.write(ia)
            st.session_state['RESPOSTA_IA']=ia
            if st.button('Nova pergunta'):
                st.session_state['indice_pergunta']+=1
                perguntas_page()
    except Exception:
        print()