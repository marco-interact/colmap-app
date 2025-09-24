import { redirect } from 'next/navigation'
import { getCurrentUser } from '@/lib/auth'
import { DashboardClient } from './dashboard-client'

export default async function DashboardPage() {
  const user = await getCurrentUser()
  
  if (!user) {
    redirect('/auth/login')
  }

  return <DashboardClient user={user} />
}
