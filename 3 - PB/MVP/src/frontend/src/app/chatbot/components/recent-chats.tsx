"use client";
import { formatDistanceToNow } from "date-fns";
import { cn } from "@/lib/utils"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Chat } from "../data";
import { Button } from "@/components/ui/button"
import { buttonVariants } from "@/components/ui/button"
import {
  ContextMenu,
  ContextMenuContent,
  ContextMenuTrigger,
} from "@/components/ui/context-menu"

import {
  AlertDialog,
  AlertDialogTrigger,
  AlertDialogContent,
  AlertDialogHeader,
  AlertDialogFooter,
  AlertDialogTitle,
  AlertDialogDescription,
  AlertDialogAction,
  AlertDialogCancel,
} from "@/components/ui/alert-dialog"

interface RecentChatsProps {
  items: Chat[]
}

export function RecentChats({ items }: RecentChatsProps) {

    const hideContextMenu = (id: string) => {
      document.getElementById(id)!.style.display = "none";
    }

   const handleDeleteChat = (id: string) => {
     console.log('Chat deleted:', id)
   }

  return ( 
    <ScrollArea>
         <div className="flex flex-col gap-2 p-4 pt-0"> 
            {items.map((item) => (
              <ContextMenu>
              <ContextMenuTrigger> 
              <button
                key={item.id}
                className={cn(
                  "flex flex-col items-start gap-2 rounded-lg border p-3 text-left text-sm transition-all hover:bg-accent",
                )}
              >                
                <div className="flex w-full flex-col gap-1">
                  <div className="flex items-center gap-x-2">
                    <div className="flex items-center gap-x-2">
                      {!item.read && (
                        <span className="flex h-2 w-2 rounded-full bg-blue-600" />
                      )}
                      <div className="font-semibold line-clamp-1">{item.name}</div>
                    </div>
                    <div
                      className={cn("ml-auto text-xs line-clamp-1")}
                    >
                      {formatDistanceToNow(new Date(item.date), {
                        addSuffix: true,
                      })}
                    </div>
                  </div>
                </div>
                <div className="line-clamp-2 text-xs text-muted-foreground">
                  {item.text.substring(0, 300)}
                </div>
              </button>  
              </ContextMenuTrigger> 
              <ContextMenuContent id={item.id}> 
                  <AlertDialog>
                  <AlertDialogTrigger asChild>
                    <Button variant="ghost" size="sm" className="text-error-foreground hover:bg-error hover:text-error-foreground w-full justify-start px-2 py-[6px] h-8"
                    >
                      Delete
                    </Button>
                  </AlertDialogTrigger>
                <AlertDialogContent>
                  <AlertDialogHeader>
                    <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
                      <AlertDialogDescription>
                        This action cannot be undone. This will permanently delete the selected chat.
                      </AlertDialogDescription>
                  </AlertDialogHeader>
                  <AlertDialogFooter>
                    <AlertDialogCancel
                    onClick={() => hideContextMenu(item.id)}
                      >
                       Abort</AlertDialogCancel>
                      <AlertDialogAction className={
                        cn(buttonVariants({ variant: "destructive" }),
                          "mt-2 sm:mt-0")}
                            onClick={() => {
                              hideContextMenu(item.id)
                              handleDeleteChat(item.id)
                            }}
                          >Delete</AlertDialogAction>
                  </AlertDialogFooter>
                </AlertDialogContent> 
                </AlertDialog>
              </ContextMenuContent> 
              </ContextMenu>          
            ))}  
          </div>   
    </ScrollArea>
  )
}