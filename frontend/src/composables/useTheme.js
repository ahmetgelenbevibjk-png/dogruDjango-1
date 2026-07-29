import{ref} from 'vue'

const isDark=ref(false)

export function useTheme() {
    const toggleTheme=()=>{
        isDark.value=!isDark.value
        const theme=isDark.value ? 'dark' : 'light'

        document.documentElement.setAttribute('data-theme',theme)
        localStorage.setItem('theme', theme)
                           }
        const initTheme=()=>{
        const savedTheme=localStorage.getItem('theme')
            if(savedTheme==='dark'){
                document.documentElement.setAttribute('data-theme','dark')
                                   }
            else {
                isDark.value=false
                document.documentElement.setAttribute('data-theme','light')
                }
                            }

        return {
        isDark,
        toggleTheme ,
        initTheme
        }
                                 }