import streamlit as st
import streamlit.components.v1 as components

# Crear el componente personalizado
_component_func = components.declare_component(
    "my_component",
    path="my_component"
)

# Función para usar el componente en Streamlit
def my_component(name=None, key=None):
    component_value = _component_func(name=name, key=key, default="")
    return component_value
