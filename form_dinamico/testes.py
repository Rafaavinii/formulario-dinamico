from selenium import webdriver

# Inicializar o driver do navegador (nesse exemplo, usaremos o Chrome)
driver = webdriver.Chrome()

# Navegar até uma URL
driver.get("https://www.exemplo.com")

# Imprimir o título da página
print(driver.title)

# Fechar o navegador
driver.quit()