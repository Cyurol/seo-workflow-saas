FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -q

# 复制代码
COPY api/ ./api/
COPY workflows/ ./workflows/
COPY docs/ ./docs/

# Railway自动设置PORT环境变量
ENV PORT=8000

# 暴露端口
EXPOSE 8000

# Railway启动命令
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
