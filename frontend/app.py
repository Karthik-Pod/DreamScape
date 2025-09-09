import streamlit as st
import requests

st.set_page_config(page_title='DreamScape', page_icon='🎬')

st.title('🎬 DreamScape: AI Movie Platform')
st.write('Basic setup complete!')

def test_backend():
    try:
        response = requests.get('http://localhost:5000/api/status', timeout=5)
        return response.json()
    except:
        return {'status': 'offline'}

backend_status = test_backend()

if backend_status['status'] == 'online':
    st.success('✅ Backend Connected!')
    st.json(backend_status)
else:
    st.error('❌ Backend Offline')
    st.info('Run: cd backend && python app.py')

st.header('🎯 Current Status')
st.success('✅ Basic Flask + Streamlit setup working!')
st.info('💡 We skipped pandas to avoid compilation issues')
st.info('🔑 Next: Get API keys and add AI features')

if st.button('🧪 Test API'):
    try:
        response = requests.get('http://localhost:5000/api/test')
        st.json(response.json())
    except:
        st.error('API test failed')
