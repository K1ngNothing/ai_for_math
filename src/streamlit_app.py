import re

import streamlit as st
from coordinator import Coordinator
from logTools import LogLevel

st.set_page_config(
    page_title="Math Problem Solver",
    page_icon="🧮",
    layout="centered"
)

st.title("🧮 Math Problem Solver")

if 'problem_text' not in st.session_state:
    st.session_state.problem_text = ""


def format_math_text(text: str) -> str:
    """Convert common LaTeX delimiters to Streamlit-friendly markdown math."""
    if not text:
        return ""

    formatted = text.strip()
    formatted = re.sub(
        r"\\\[(.*?)\\\]",
        lambda match: f"\n$$\n{match.group(1).strip()}\n$$\n",
        formatted,
        flags=re.DOTALL,
    )
    formatted = re.sub(
        r"\\\((.*?)\\\)",
        lambda match: f"${match.group(1).strip()}$",
        formatted,
        flags=re.DOTALL,
    )
    return formatted


def set_example(example_text):
    st.session_state.problem_text = example_text


examples = [
    "Для скольких целых значений $x$ не выполняется неравенство $5x^{2}+19x+16 > 20$?",
    "В прямоугольном треугольнике $ABC$, где $\\angle A = 90^\\circ$, известно, что $AB = 16$ и $BC = 24$. Найдите $\\sin A$.",
    "Пусть $a$ и $b$ — два действительных значения $x$, для которых \\[\\sqrt[3]{x} + \\sqrt[3]{20 - x} = 2\\] Меньшее из этих двух значений можно представить в виде $p - \\sqrt{q}$, где $p$ и $q$ — целые числа. Найдите $p + q$.",
]

st.write("Примеры задач:")
example_columns = st.columns(len(examples))
for i, (column, example) in enumerate(zip(example_columns, examples)):
    with column:
        st.button(
            f"Пример {i+1}",
            on_click=set_example,
            args=(example,),
            key=f"example_{i}",
            use_container_width=True,
        )

problem = st.text_area(
    "Введите условие задачи:",
    value=st.session_state.problem_text,
    height=75,
    placeholder="Например: \"Реши квадратное уравнение: $x^2 - 5x + 6 = 0$\""
)

if problem.strip():
    with st.container(border=True):
        st.caption("Предпросмотр условия")
        st.markdown(format_math_text(problem))

if st.button("Решить", type="primary"):
    if problem.strip():
        try:
            coordinator = Coordinator(LogLevel.RELEASE)

            with st.spinner("Решаю..."):
                result = coordinator.solve(problem)

            st.markdown("### Результат:")

            if isinstance(result, dict):
                if 'answer' in result and result['answer']:
                    formatted_answer = format_math_text(result['answer']).strip()
                    st.markdown(f"**Ответ:** {formatted_answer}")

                if 'solution' in result and result['solution']:
                    with st.expander("Показать решение"):
                        st.markdown(format_math_text(result['solution']))
            else:
                formatted_answer = format_math_text(str(result)).strip()
                st.markdown(f"**Ответ:** {formatted_answer}")

        except Exception as e:
            st.error(f"Ошибка: {str(e)}")
    else:
        st.warning("Введите задачу для решения")
