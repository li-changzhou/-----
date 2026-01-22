/* Event Countdown Tool - 前端应用逻辑 */

const API_BASE = '/api';
let currentEvents = [];
let editingEventName = null;

// ==================== 初始化 ====================

document.addEventListener('DOMContentLoaded', function() {
    console.log('应用已启动');
    // 加载初始数据
    loadEvents();
    loadStats();
    
    // 设置实时更新 (每 5 秒更新一次统计信息)
    setInterval(loadStats, 5000);
    
    // 搜索功能
    document.getElementById('search-input').addEventListener('input', handleSearch);
});

// ==================== 事件加载 ====================

async function loadEvents(filterStatus = null) {
    try {
        const url = filterStatus 
            ? `${API_BASE}/events?status=${filterStatus}`
            : `${API_BASE}/events`;
        
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error('无法加载事件');
        }
        
        const data = await response.json();
        currentEvents = data.events;
        
        renderEvents(currentEvents);
    } catch (error) {
        console.error('加载事件失败:', error);
        showNotification('加载事件失败', 'error');
    }
}

async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        
        if (!response.ok) {
            throw new Error('无法加载统计数据');
        }
        
        const stats = await response.json();
        
        document.getElementById('stat-total').textContent = stats.total_events;
        document.getElementById('stat-active').textContent = stats.active_events;
        document.getElementById('stat-expired').textContent = stats.expired_events;
        
        if (stats.next_event) {
            document.getElementById('stat-next').textContent = 
                `${stats.next_event} (${stats.next_event_days} 天)`;
        } else {
            document.getElementById('stat-next').textContent = '无';
        }
    } catch (error) {
        console.error('加载统计数据失败:', error);
    }
}

// ==================== 事件渲染 ====================

function renderEvents(events) {
    const container = document.getElementById('events-container');
    const emptyState = document.getElementById('empty-state');
    
    if (events.length === 0) {
        container.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }
    
    emptyState.style.display = 'none';
    
    container.innerHTML = events.map(event => createEventCard(event)).join('');
}

function createEventCard(event) {
    const daysRemaining = event.days_remaining;
    const isExpired = event.status === 'EXPIRED';
    const isCurrent = event.status === 'CURRENT';
    
    const cardClass = isExpired ? 'expired' : (isCurrent ? 'current' : '');
    const statusClass = event.status.toLowerCase();
    const countdownClass = isExpired ? 'expired' : '';
    
    const statusText = {
        'ACTIVE': '进行中',
        'CURRENT': '即将到来',
        'EXPIRED': '已过期'
    }[event.status] || '未知';
    
    return `
        <div class="event-card ${cardClass}">
            <div class="event-header">
                <h3 class="event-name">${escapeHtml(event.name)}</h3>
                <span class="event-status ${statusClass}">${statusText}</span>
            </div>
            <div class="event-date">📅 ${formatDate(event.date)}</div>
            <div class="event-countdown">
                <div>
                    <div class="countdown-value ${countdownClass}">${daysRemaining}</div>
                    <div class="countdown-label">${daysRemaining === 0 ? '今天就是！' : (daysRemaining === 1 ? '明天' : '天')}</div>
                </div>
            </div>
            <div class="event-actions">
                <button class="btn btn-secondary" onclick="openEditModal('${escapeHtml(event.name)}', '${event.date}')">✏️ 编辑</button>
                <button class="btn btn-danger" onclick="openDeleteModal('${escapeHtml(event.name)}')">🗑️ 删除</button>
            </div>
        </div>
    `;
}

// ==================== 搜索功能 ====================

function handleSearch(event) {
    const searchTerm = event.target.value.toLowerCase();
    
    if (!searchTerm) {
        renderEvents(currentEvents);
        return;
    }
    
    const filtered = currentEvents.filter(event => 
        event.name.toLowerCase().includes(searchTerm)
    );
    
    renderEvents(filtered);
}

// ==================== 新建事件 ====================

function openAddModal() {
    document.getElementById('add-form').reset();
    
    // 设置默认日期为明天
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    document.getElementById('event-date').valueAsDate = tomorrow;
    
    document.getElementById('add-modal').classList.add('open');
}

function closeAddModal() {
    document.getElementById('add-modal').classList.remove('open');
}

async function handleAddEvent(event) {
    event.preventDefault();
    
    const name = document.getElementById('event-name').value.trim();
    const dateStr = document.getElementById('event-date').value;
    
    if (!name || !dateStr) {
        showNotification('请输入事件名称和日期', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/events`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                date: dateStr
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || '创建事件失败');
        }
        
        closeAddModal();
        showNotification(`✅ 事件 "${name}" 已创建`, 'success');
        await loadEvents();
        await loadStats();
    } catch (error) {
        console.error('创建事件失败:', error);
        showNotification(error.message || '创建事件失败', 'error');
    }
}

// ==================== 编辑事件 ====================

function openEditModal(name, date) {
    editingEventName = name;
    document.getElementById('edit-event-name').value = name;
    document.getElementById('edit-event-date').value = date;
    document.getElementById('edit-modal').classList.add('open');
}

function closeEditModal() {
    document.getElementById('edit-modal').classList.remove('open');
    editingEventName = null;
}

async function handleEditEvent(event) {
    event.preventDefault();
    
    const newDate = document.getElementById('edit-event-date').value;
    
    if (!editingEventName || !newDate) {
        showNotification('请输入新的日期', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/events/${encodeURIComponent(editingEventName)}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                date: newDate
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || '更新事件失败');
        }
        
        closeEditModal();
        showNotification(`✅ 事件 "${editingEventName}" 已更新`, 'success');
        await loadEvents();
        await loadStats();
    } catch (error) {
        console.error('更新事件失败:', error);
        showNotification(error.message || '更新事件失败', 'error');
    }
}

// ==================== 删除事件 ====================

function openDeleteModal(name) {
    editingEventName = name;
    document.getElementById('delete-confirm-text').textContent = 
        `确定要删除事件 "${name}" 吗？此操作无法撤销。`;
    document.getElementById('delete-modal').classList.add('open');
}

function closeDeleteModal() {
    document.getElementById('delete-modal').classList.remove('open');
    editingEventName = null;
}

async function confirmDelete() {
    if (!editingEventName) {
        return;
    }
    
    try {
        const response = await fetch(
            `${API_BASE}/events/${encodeURIComponent(editingEventName)}`,
            { method: 'DELETE' }
        );
        
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || '删除事件失败');
        }
        
        closeDeleteModal();
        showNotification(`✅ 事件 "${editingEventName}" 已删除`, 'success');
        await loadEvents();
        await loadStats();
    } catch (error) {
        console.error('删除事件失败:', error);
        showNotification(error.message || '删除事件失败', 'error');
    }
}

// ==================== 刷新 ====================

async function refreshEvents() {
    await loadEvents();
    await loadStats();
    showNotification('✅ 已刷新', 'success');
}

// ==================== 工具函数 ====================

function formatDate(dateStr) {
    try {
        const date = new Date(dateStr + 'T00:00:00');
        return date.toLocaleDateString('zh-CN', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            weekday: 'short'
        });
    } catch (e) {
        return dateStr;
    }
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type}`;
    
    // 3 秒后隐藏
    setTimeout(() => {
        notification.classList.add('hidden');
    }, 3000);
}

// 按 Escape 关闭对话框
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeAddModal();
        closeEditModal();
        closeDeleteModal();
    }
});
