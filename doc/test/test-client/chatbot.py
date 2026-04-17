#!/usr/bin/env python3
"""
对话式知识问答系统

支持 OpenAI 兼容 API，可通过配置文件自定义 API URL 和 Key。
支持上下文记忆功能，自动保存对话历史到 memory.md。
"""

import os
import sys
import yaml
import argparse
from datetime import datetime
from typing import List, Dict, Any, Optional
from openai import OpenAI


class MemoryManager:
    """记忆管理器
    
    负责将对话历史保存到 memory.md 文件，支持自动遗忘（超过1000行时清理）。
    """
    
    MAX_LINES = 1000  # 最大行数限制
    
    def __init__(self, memory_file: str = "memory.md"):
        """初始化记忆管理器
        
        Args:
            memory_file: 记忆文件路径
        """
        self.memory_file = memory_file
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """确保记忆文件存在"""
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                f.write("# 对话记忆\n\n")
    
    def _count_lines(self) -> int:
        """计算文件当前行数"""
        try:
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                return len(f.readlines())
        except Exception:
            return 0
    
    def _forget_old_memories(self):
        """遗忘旧记忆（当超过最大行数时）"""
        current_lines = self._count_lines()
        if current_lines <= self.MAX_LINES:
            return
        
        try:
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 保留文件头（标题）和最近的记忆
            # 找到需要保留的内容（保留最后 500 行）
            header_lines = []
            content_lines = []
            
            for i, line in enumerate(lines):
                if i < 2:  # 保留 "# 对话记忆\n\n"
                    header_lines.append(line)
                else:
                    content_lines.append(line)
            
            # 只保留后 500 行内容
            keep_lines = content_lines[-500:] if len(content_lines) > 500 else content_lines
            
            # 添加遗忘标记
            forget_notice = f"\n> 注意：由于记忆超过 {self.MAX_LINES} 行，已自动遗忘较早的对话。\n\n"
            
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                f.writelines(header_lines)
                f.write(forget_notice)
                f.writelines(keep_lines)
                
        except Exception as e:
            print(f"⚠️  遗忘旧记忆时出错: {e}")
    
    def add_conversation(self, user_input: str, assistant_response: str, model: str = "unknown"):
        """添加对话到记忆
        
        Args:
            user_input: 用户输入
            assistant_response: 助手回复
            model: 使用的模型名称
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 格式化对话记录
        entry = f"## {timestamp} | 模型: {model}\n\n"
        entry += f"**用户**: {user_input}\n\n"
        entry += f"**助手**: {assistant_response[:500]}"  # 限制单条回复长度
        if len(assistant_response) > 500:
            entry += "..."
        entry += "\n\n---\n\n"
        
        try:
            # 先检查是否需要遗忘
            self._forget_old_memories()
            
            # 追加到文件
            with open(self.memory_file, 'a', encoding='utf-8') as f:
                f.write(entry)
                
        except Exception as e:
            print(f"⚠️  保存记忆时出错: {e}")
    
    def get_recent_context(self, num_exchanges: int = 3) -> List[Dict[str, str]]:
        """获取最近的对话上下文
        
        Args:
            num_exchanges: 获取的对话轮数
            
        Returns:
            对话消息列表
        """
        messages = []
        
        try:
            if not os.path.exists(self.memory_file):
                return messages
            
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 简单解析最近的对话
            # 按分隔符分割
            exchanges = content.split("\n---\n")
            
            # 取最后 num_exchanges 个
            recent = exchanges[-num_exchanges:] if len(exchanges) > num_exchanges else exchanges
            
            for exchange in recent:
                lines = exchange.strip().split('\n')
                user_msg = None
                assistant_msg = None
                
                for line in lines:
                    if line.startswith('**用户**: '):
                        user_msg = line[9:].strip()
                    elif line.startswith('**助手**: '):
                        assistant_msg = line[9:].strip()
                
                if user_msg and assistant_msg:
                    messages.append({"role": "user", "content": user_msg})
                    messages.append({"role": "assistant", "content": assistant_msg})
                    
        except Exception as e:
            print(f"⚠️  读取记忆时出错: {e}")
        
        return messages
    
    def clear_memory(self):
        """清空所有记忆"""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                f.write("# 对话记忆\n\n")
            print("✅ 记忆已清空")
        except Exception as e:
            print(f"❌ 清空记忆失败: {e}")
    
    def show_memory_stats(self):
        """显示记忆统计"""
        lines = self._count_lines()
        size = os.path.getsize(self.memory_file) if os.path.exists(self.memory_file) else 0
        print(f"\n📊 记忆统计:")
        print(f"  文件: {self.memory_file}")
        print(f"  行数: {lines} / {self.MAX_LINES}")
        print(f"  大小: {size / 1024:.1f} KB")
        print()


class ChatBot:
    """对话式知识问答系统"""
    
    def __init__(self, config_path: str = "config.yaml", memory_file: str = "memory.md"):
        """初始化聊天机器人
        
        Args:
            config_path: 配置文件路径
            memory_file: 记忆文件路径
        """
        self.config = self._load_config(config_path)
        self.client = self._init_client()
        self.memory = MemoryManager(memory_file)
        self.messages: List[Dict[str, str]] = []
        self._init_conversation()
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置文件"""
        if not os.path.exists(config_path):
            print(f"❌ 配置文件不存在: {config_path}")
            print("请复制 config.yaml.example 为 config.yaml 并配置您的 API 信息")
            sys.exit(1)
        
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _init_client(self) -> OpenAI:
        """初始化 OpenAI 客户端"""
        api_config = self.config.get('api', {})
        
        base_url = api_config.get('base_url', 'http://127.0.0.1:8080')
        api_key = api_config.get('api_key', '')
        timeout = api_config.get('timeout', 30)
        
        if not api_key:
            print("❌ 请在配置文件中设置 api_key")
            sys.exit(1)
        
        return OpenAI(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout
        )
    
    def _init_conversation(self):
        """初始化对话历史"""
        system_prompt = self.config.get('chat', {}).get('system_prompt', '')
        if system_prompt:
            self.messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # 加载最近的记忆作为上下文
        memory_context = self.config.get('chat', {}).get('memory_context', 3)
        if memory_context > 0:
            recent_memories = self.memory.get_recent_context(memory_context)
            if recent_memories:
                # 添加记忆提示
                self.messages.append({
                    "role": "system",
                    "content": "以下是与用户的最近对话历史，供你参考："
                })
                self.messages.extend(recent_memories)
    
    def _get_model(self) -> str:
        """获取模型名称"""
        return self.config.get('api', {}).get('model', 'qwen3.6-plus')
    
    def _get_chat_params(self) -> Dict[str, Any]:
        """获取对话参数"""
        chat_config = self.config.get('chat', {})
        return {
            "temperature": chat_config.get('temperature', 0.7),
            "max_tokens": chat_config.get('max_tokens', 2000)
        }
    
    def _manage_history(self):
        """管理对话历史，防止过长"""
        max_history = self.config.get('chat', {}).get('max_history', 10)
        # 保留 system 消息和最近的消息
        if len(self.messages) > max_history + 1:
            system_msg = self.messages[0] if self.messages[0]['role'] == 'system' else None
            self.messages = self.messages[-max_history:]
            if system_msg:
                self.messages.insert(0, system_msg)
    
    def send_message(self, user_input: str) -> str:
        """发送消息并获取回复
        
        Args:
            user_input: 用户输入
            
        Returns:
            助手回复
        """
        # 添加用户消息
        self.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # 管理历史记录
        self._manage_history()
        
        try:
            # 调用 API
            response = self.client.chat.completions.create(
                model=self._get_model(),
                messages=self.messages,
                **self._get_chat_params()
            )
            
            # 获取回复
            assistant_message = response.choices[0].message
            content = assistant_message.content
            
            # 添加助手消息到历史
            self.messages.append({
                "role": "assistant",
                "content": content
            })
            
            # 保存到记忆
            self.memory.add_conversation(user_input, content, self._get_model())
            
            return content
            
        except Exception as e:
            error_msg = f"请求出错: {str(e)}"
            print(f"\n❌ {error_msg}")
            return error_msg
    
    def clear_history(self):
        """清空对话历史"""
        system_msg = None
        if self.messages and self.messages[0]['role'] == 'system':
            system_msg = self.messages[0]
        
        self.messages = []
        if system_msg:
            self.messages.append(system_msg)
        
        print("✅ 对话历史已清空")
    
    def clear_memory(self):
        """清空记忆"""
        self.memory.clear_memory()
    
    def print_welcome(self):
        """打印欢迎信息"""
        ui_config = self.config.get('ui', {})
        welcome = ui_config.get('welcome_message', '欢迎使用！')
        separator = ui_config.get('separator', '─' * 50)
        
        print()
        print(separator)
        print(welcome)
        print(separator)
        print()
        print("命令:")
        print("  /clear    - 清空对话历史")
        print("  /memory   - 显示记忆统计")
        print("  /forget   - 清空所有记忆")
        print("  /config   - 显示当前配置")
        print("  quit      - 退出程序")
        print(separator)
        print()
    
    def print_config(self):
        """打印当前配置"""
        api_config = self.config.get('api', {})
        print("\n📋 当前配置:")
        print(f"  API URL: {api_config.get('base_url', 'N/A')}")
        print(f"  模型: {api_config.get('model', 'N/A')}")
        print(f"  历史消息数: {len(self.messages)}")
        print()
    
    def run(self):
        """运行对话循环"""
        self.print_welcome()
        
        ui_config = self.config.get('ui', {})
        prompt = ui_config.get('prompt', '你: ')
        assistant_prefix = ui_config.get('assistant_prefix', '助手: ')
        
        while True:
            try:
                # 获取用户输入
                user_input = input(prompt).strip()
                
                if not user_input:
                    continue
                
                # 处理命令
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 再见！")
                    break
                
                if user_input == '/clear':
                    self.clear_history()
                    continue
                
                if user_input == '/memory':
                    self.memory.show_memory_stats()
                    continue
                
                if user_input == '/forget':
                    self.clear_memory()
                    continue
                
                if user_input == '/config':
                    self.print_config()
                    continue
                
                # 发送消息并显示回复
                response = self.send_message(user_input)
                print(f"\n{assistant_prefix}{response}\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 再见！")
                break
            except EOFError:
                print("\n\n👋 再见！")
                break


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='对话式知识问答系统')
    parser.add_argument(
        '-c', '--config',
        default='config.yaml',
        help='配置文件路径 (默认: config.yaml)'
    )
    
    args = parser.parse_args()
    
    # 创建并运行聊天机器人
    bot = ChatBot(config_path=args.config)
    bot.run()


if __name__ == '__main__':
    main()
