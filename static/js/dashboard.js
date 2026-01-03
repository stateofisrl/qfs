/* Dashboard JavaScript */

document.addEventListener('DOMContentLoaded', function () {
    loadDashboardData();
    // Auto-refresh dashboard data every 30 seconds
    setInterval(loadDashboardData, 30000);
});

async function loadDashboardData() {
    try {
        // Load user balance and stats from API
        console.log('Loading dashboard data...');
        console.log('Token available:', !!localStorage.getItem('token'));
        
        const meResponse = await fetchAPI('/users/me/');
        console.log('User data received:', meResponse);
        displayBalance(meResponse);

        // Load active investments
        try {
            const investmentsResponse = await fetchAPI('/investments/my-investments/active_investments/');
            console.log('Investments data:', investmentsResponse);
            displayActiveInvestments(investmentsResponse);
        } catch (invErr) {
            console.error('Error loading investments:', invErr);
            displayActiveInvestments([]);
        }

        // Load recent deposits
        try {
            const depositsResponse = await fetchAPI('/deposits/my_deposits/');
            console.log('Deposits data:', depositsResponse);
            displayRecentDeposits(depositsResponse);
        } catch (depErr) {
            console.error('Error loading deposits:', depErr);
            displayRecentDeposits([]);
        }
    } catch (error) {
        console.error('Error loading dashboard:', error);
        console.warn('If you see this, the API call failed. Make sure you are logged in and have a valid token.');
    }
}

function displayBalance(user) {
    // Update balance cards with data from API
    console.log('Displaying balance, user object:', user);
    const balanceEl = document.querySelector('[data-balance]');
    const investedEl = document.querySelector('[data-invested]');
    const earningsEl = document.querySelector('[data-earnings]');
    
    console.log('Balance element:', balanceEl);
    console.log('Invested element:', investedEl);
    console.log('Earnings element:', earningsEl);
    
    if (balanceEl && user.balance !== undefined) {
        const newBalance = parseFloat(user.balance).toFixed(2);
        const formattedBalance = '$' + newBalance;
        console.log('Setting balance to:', formattedBalance);
        
        // Add animation if value changed
        if (balanceEl.textContent !== formattedBalance) {
            balanceEl.style.transition = 'all 0.3s ease';
            balanceEl.style.transform = 'scale(1.05)';
            setTimeout(() => {
                balanceEl.style.transform = 'scale(1)';
            }, 300);
        }
        balanceEl.textContent = formattedBalance;
    } else {
        console.warn('Balance element not found or user.balance is undefined');
    }
    
    if (investedEl && user.total_invested !== undefined) {
        const newInvested = parseFloat(user.total_invested).toFixed(2);
        const formattedInvested = '$' + newInvested;
        console.log('Setting total invested to:', formattedInvested);
        
        // Add animation if value changed
        if (investedEl.textContent !== formattedInvested) {
            investedEl.style.transition = 'all 0.3s ease';
            investedEl.style.transform = 'scale(1.05)';
            setTimeout(() => {
                investedEl.style.transform = 'scale(1)';
            }, 300);
        }
        investedEl.textContent = formattedInvested;
    }
    
    if (earningsEl && user.total_earnings !== undefined) {
        const newEarnings = parseFloat(user.total_earnings).toFixed(2);
        const formattedEarnings = '$' + newEarnings;
        console.log('Setting total earnings to:', formattedEarnings);
        
        // Add animation if value changed
        if (earningsEl.textContent !== formattedEarnings) {
            earningsEl.style.transition = 'all 0.3s ease';
            earningsEl.style.transform = 'scale(1.05)';
            setTimeout(() => {
                earningsEl.style.transform = 'scale(1)';
            }, 300);
        }
        earningsEl.textContent = formattedEarnings;
    }
}

function displayActiveInvestments(investments) {
    const container = document.getElementById('investments-list');
    
    if (!investments || investments.length === 0) {
        container.innerHTML = '<div class="card-body"><p class="text-muted">No active investments yet</p></div>';
        return;
    }

    let html = '<div class="list-group">';
    investments.forEach(inv => {
        html += `
            <div class="list-group-item">
                <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1">${inv.plan_name}</h6>
                    <small>${formatDate(inv.start_date)}</small>
                </div>
                <p class="mb-1"><strong>Amount:</strong> ${formatCurrency(inv.amount)}</p>
                <p class="mb-1"><strong>ROI:</strong> ${inv.plan_roi}%</p>
                <small><strong>Expected Return:</strong> ${formatCurrency(inv.expected_return)}</small>
            </div>
        `;
    });
    html += '</div>';
    container.innerHTML = html;
}

function displayRecentDeposits(deposits) {
    const container = document.getElementById('deposits-list');
    
    if (!deposits || deposits.length === 0) {
        container.innerHTML = '<div class="card-body"><p class="text-muted">No deposits yet</p></div>';
        return;
    }

    let html = '<div class="list-group">';
    deposits.slice(0, 3).forEach(deposit => {
        const walletAddr = deposit.wallet_address ? `<div class="mt-1"><code style="word-break: break-all; font-size:0.8rem;">${deposit.wallet_address}</code></div>` : '';
        html += `
            <div class="list-group-item">
                <div class="d-flex w-100 justify-content-between align-items-center">
                    <div>
                        <h6 class="mb-1">${deposit.cryptocurrency}</h6>
                        <small>${formatDate(deposit.created_at)}</small>
                        ${walletAddr}
                    </div>
                    <div class="text-end">
                        <strong>${formatCurrency(deposit.amount)}</strong>
                        <br>
                        ${getStatusBadge(deposit.status)}
                    </div>
                </div>
            </div>
        `;
    });
    html += '</div>';
    container.innerHTML = html;
}
