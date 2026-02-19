#!/usr/bin/env python3
import re

file_path = '/Users/junjunyi/src-code/flearn/front-tutorial/sections/frameworks.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the main framework table tbody section
old_tbody = '''<tbody>
                            <tr>
                                <td><strong>React</strong></td>
                                <td>组件化开发、JSX 语法、Props 属性、State 状态、Hooks(useState/useEffect/useContext 等)</td>
                                <td><code>React</code> <code>JSX</code> <code>Hooks</code></td>
                            </tr>
                            <tr>
                                <td><strong>Next.js 15+</strong></td>
                                <td>App Router 路由系统、Server Components 服务器组件、Server Actions 服务端动作、SSR/SSG 混合渲染</td>
                                <td><code>App Router</code> <code>Server Components</code></td>
                            </tr>
                            <tr>
                                <td><strong>Vue 3</strong></td>
                                <td>Composition API、Setup 语法糖、响应式系统 ref/reactive、Pinia 状态管理、Vue Router</td>
                                <td><code>Vue 3</code> <code>Composition API</code></td>
                            </tr>
                            <tr>
                                <td><strong>Nuxt 4</strong></td>
                                <td>混合渲染模式、Vapor Mode 性能优化、文件目录约定、自动化路由和 API 生成</td>
                                <td><code>Nuxt</code> <code>Vapor Mode</code></td>
                            </tr>
                            <tr>
                                <td><strong>TanStack Query</strong></td>
                                <td>React Query 数据获取、缓存管理、自动重新获取、乐观更新、服务器状态管理标准</td>
                                <td><code>React Query</code> <code>TanStack Query</code></td>
                            </tr>
                        </tbody>'''

new_tbody = '''<tbody>
                            <tr>
                                <td><strong>React 19</strong></td>
                                <td>Compiler 自动优化、use 钩子、Actions 服务器动作、Document 元数据、组件式服务端组件</td>
                                <td><code>React 19</code> <code>use()</code> <code>Actions</code></td>
                            </tr>
                            <tr>
                                <td><strong>Next.js 15+</strong></td>
                                <td>App Router 路由系统、Server Components 服务器组件、Server Actions 服务端动作、SSR/SSG 混合渲染</td>
                                <td><code>App Router</code> <code>Server Components</code></td>
                            </tr>
                            <tr>
                                <td><strong>Vue 3.5+</strong></td>
                                <td>Composition API、Setup 语法糖、响应式系统 ref/reactive、Pinia 状态管理、Vue Router</td>
                                <td><code>Vue 3.5+</code> <code>Composition API</code></td>
                            </tr>
                            <tr>
                                <td><strong>Nuxt 4</strong></td>
                                <td>混合渲染模式、Vapor Mode 性能优化、文件目录约定、自动化路由和 API 生成</td>
                                <td><code>Nuxt</code> <code>Vapor Mode</code></td>
                            </tr>
                            <tr>
                                <td><strong>Svelte 5</strong></td>
                                <td>Runes 响应式原语、Snippets 片段、$state 状态、$derived 派生、编译时框架</td>
                                <td><code>$state</code> <code>$derived</code> <code>Runes</code></td>
                            </tr>
                            <tr>
                                <td><strong>SolidJS 1.8+</strong></td>
                                <td>细粒度响应式、Signals 信号、无虚拟 DOM、JSX 语法、编译时优化</td>
                                <td><code>createSignal</code> <code>createEffect</code> <code>Signals</code></td>
                            </tr>
                            <tr>
                                <td><strong>Qwik</strong></td>
                                <td>可恢复性架构、零水合、QRL 惰性加载、序列化应用状态、即时交互</td>
                                <td><code>Qwik</code> <code>QRL</code> <code>零水合</code></td>
                            </tr>
                            <tr>
                                <td><strong>TanStack Query</strong></td>
                                <td>React Query 数据获取、缓存管理、自动重新获取、乐观更新、服务器状态管理标准</td>
                                <td><code>React Query</code> <code>TanStack Query</code></td>
                            </tr>
                        </tbody>'''

if old_tbody in content:
    content = content.replace(old_tbody, new_tbody)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully replaced the main framework table")
else:
    print("Could not find the exact pattern to replace")
