import openai
import os
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

openai.api_key = os.getenv('API_KEY')

llm = ChatOpenAI(api_key=openai.api_key, model="gpt-4o", temperature=0.1, max_tokens=1000, timeout=None, max_retries=2)

def analyze_feedback(text):
    template = """
        Você é um analista de uma startup que oferece um aplicativo focado em bem-estar e saúde mental chamada AluMind. 
        Seu trabalho é analisar o feedback do usuário e fornecer:
        - Um sentimento
        - Um código
        - Uma razão

        O sentimento fornecido deve ser uma das seguintes categorias:
        - POSITIVO: O feedback deve ter um caráter positivo, elogiando ou destacando positivamente características do aplicativo. Exemplo: Gosto muito de usar o Alumind!
        - NEGATIVO: O feedback deve ter um caráter negativo, apontando problemas ou realizando críticas ao sistema. Exemplo: O botão de cadastro não funciona.
        - INCONCLUSIVO: O feedback deve ter um caráter neutro, ou seja, nem positivo nem negativo. Além disso, pode ser que o feedback não tenha informações suficientes para concluir seu caráter. Exemplo: Não entendi como usar o novo menu.

        Já o código deve ser fornecido seguindo a seguinte regra:
        - Deve ser um código de no máximo duas palavras, sendo a primeira palavra um verbo no infinitivo e a segunda um substantivo. O formato do código deve seguir um dos 3 modelos:
            - VERBO_SUBSTANTIVO
            - VERBO
            - SUBSTANTIVO
            Exemplos: EDITAR_PERFIL, MENU, CADASTRAR
            
        Já a razão deve ser um resumo do feedback. Exemplo: O usuário gostaria de realizar a edição do próprio perfil.
            
        Não utilize o caracter ` nem a palavra json na sua resposta.    
            
        Sendo assim, analise o feedback fornecido e forneça uma saída, conforme o exemplo a seguir:
        {{"sentiment": "POSITIVO", "requested_features": [{{"code": "EDITAR_MENU", "reason": "O usuário gostaria de realizar a edição do próprio perfil."}}]}}

        Feedback: {text}

"""

    try:
        prompt = PromptTemplate(input_variables=["text"], template=template)
        chain = LLMChain(llm=llm, prompt=prompt)

        return str(chain.run({"text": text}))
        
    except Exception as e:
        return {"error": "Ocorreu um erro durante a análise do feedback"}
    
def analyze_spam(text):
    template = """
        Você é um analista de uma startup que oferece um aplicativo focado em bem-estar e saúde mental chamada AluMind.
        Entenda como SPAM o texto que não condiza com o contexto da AluMind.
        Entenda como SPAM também textos que contenham palavras de baixo calão.
        Sua resposta deve ser apenas Sim ou Não.
        Caso você entenda que o conteúdo não diz respeito ao aplicativo, automaticamente dê a resposta Sim.
        Seu trabalho agora é classificar o texto abaixo como:
        
        Feedback: {text}
    
    """
    
    try:
        prompt = PromptTemplate(input_variables=["text"], template=template)
        chain = LLMChain(llm=llm, prompt=prompt)

        return chain.run({"text": text})
        
    except Exception as e:
        return {"error": "Ocorreu um erro durante a análise do feedback"}
