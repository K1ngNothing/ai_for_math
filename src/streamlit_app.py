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

def set_example(example_text):
    st.session_state.problem_text = example_text

examples = [
    "Let $a$ and $b$ be the two real values of $x$ for which\\[\\sqrt[3]{x} + \\sqrt[3]{20 - x} = 2\\]The smaller of the two values can be expressed as $p - \\sqrt{q}$, where $p$ and $q$ are integers. Compute $p + q$.",
    "For how many integer values of $x$ is $5x^{2}+19x+16 > 20$ not satisfied?",
    "In right triangle $ABC$ with $\\angle A = 90^\\circ$, we have $AB =16$ and $BC = 24$. Find $\\sin A$."
]

st.write("Примеры задач:")
for i, example in enumerate(examples):
    st.button(
        f"Пример {i+1}",
        on_click=set_example,
        args=(example,),
        key=f"example_{i}"
    )

problem = st.text_area(
    "Введите математическую задачу:",
    value=st.session_state.problem_text,
    height=150,
    placeholder="Например: Solve for x: $x^2 - 5x + 6 = 0$"
)

if st.button("Решить", type="primary"):
    if problem.strip():
        try:
            coordinator = Coordinator(LogLevel.RELEASE)

            with st.spinner("Решаю..."):
                result = coordinator.solve(problem)

            st.markdown("### Результат:")

            if isinstance(result, dict):
                if 'answer' in result and result['answer']:
                    st.markdown(f"**Ответ:** `{result['answer']}`")

                if 'solution' in result and result['solution']:
                    with st.expander("Показать полное решение"):
                        st.markdown(result['solution'])
            else:
                st.markdown(f"**Ответ:** `{result}`")

        except Exception as e:
            st.error(f"Ошибка: {str(e)}")
    else:
        st.warning("Введите задачу для решения")
