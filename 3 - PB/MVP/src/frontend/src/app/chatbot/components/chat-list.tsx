"use client"

import { cn } from "@/lib/utils"
import { ScrollArea } from "@/components/ui/scroll-area"

import { ChatOperationResponse, ChatPreview } from "@/types/types";
import { CopyXIcon, ListTodoIcon, Search, Undo2Icon } from "lucide-react";
import { Input } from "@/components/ui/input";
import { useEffect, useState } from 'react';
import { Button, buttonVariants } from "@/components/ui/button";
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from "@/components/ui/alert-dialog";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { deleteChats } from "@/lib/actions";
import { toast } from "sonner";
import { ChatItem } from "./chat-item";
import { useRouter } from "next/navigation";

interface ChatListProps {
  chatPreviews: ChatPreview[]
}

export function ChatList({ chatPreviews }: ChatListProps) {
  const router = useRouter()
  const [filteredChats, setFilteredChats] = useState(chatPreviews)

  const [isBeingSelected, setIsBeingSelected] = useState(false)
  const [selectedChats, setSelectedChats] = useState<number[]>([])

  const onDeleteSubmit = async () => {
    setIsBeingSelected(false);

    const toastId = toast.loading("Loading...", {
      description: "Deleting chats."
    })

    let results: ChatOperationResponse[]
    try {
      results = await deleteChats(selectedChats)
    } catch (e) {
      toast.error("An error occurred", {
        description: "Please try again later.",
        id: toastId
      })
      return
    }

    toast.dismiss(toastId)

    results.forEach(result => {
      if (!result || !result.status) {
        toast.error("An error occurred", {
          description: "Error while renaming the chat:" + result.message,
        })
        return
      } else {
        toast.success("Operation successful", {
          description: "Chat has been deleted.",
        })
      }
    })
    setSelectedChats([]);
    router.push(`/chatbot`)
  }

  useEffect(() => {
    setFilteredChats(chatPreviews)
  }, [chatPreviews])

  const toggleOnSelect = (chatId: number) => {
    if (selectedChats.includes(chatId)) {
      setSelectedChats(selectedChats.filter((selectedChatId) => selectedChatId !== chatId))
    } else {
      setSelectedChats([...selectedChats, chatId])
    }
  }

  return (
    <div className="flex h-full flex-col overflow-auto">
      <div
        className="flex w-full space-x-2 bg-background/95 p-4 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="relative w-full">
          <Search
            className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground"
          />
          <Input
            placeholder="Search"
            className="pl-8"
            onChange={(e) => {
              setFilteredChats(chatPreviews.filter((chatPreview) => chatPreview.title.toLowerCase().includes(e.target.value.toLowerCase())))
            }}
          />
        </div>
        {
          isBeingSelected ?
            <div className="flex space-x-2">
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    variant="secondary"
                    size="icon"
                    onClick={() => {
                      setIsBeingSelected(false)
                      setSelectedChats([])
                    }}
                  >
                    <Undo2Icon className="h-4 w-4 min-w-[40px]" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent side="left">Abort</TooltipContent>
              </Tooltip>
              <AlertDialog>
                <AlertDialogTrigger asChild>
                  <Button
                    disabled={selectedChats.length === 0}
                    variant="destructive"
                    size="icon"
                    className="min-w-[40px]"
                  >
                    <CopyXIcon className="h-4 w-4" />
                  </Button>
                </AlertDialogTrigger>
                <AlertDialogContent>
                  <AlertDialogHeader>
                    <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
                    <AlertDialogDescription>
                      This action cannot be undone. This will permanently delete the selected chats.
                    </AlertDialogDescription>
                  </AlertDialogHeader>
                  <AlertDialogFooter>
                    <AlertDialogCancel id="dialog-cancel">Abort</AlertDialogCancel>
                    <AlertDialogAction id="dialog-action"
                      className={cn(buttonVariants({ variant: "destructive" }), "mt-2 sm:mt-0")}
                      onClick={() => onDeleteSubmit()}
                    >Delete
                    </AlertDialogAction>
                  </AlertDialogFooter>
                </AlertDialogContent>
              </AlertDialog>
            </div>
            :
            <Tooltip>
              <TooltipTrigger asChild>
                <Button
                  variant={isBeingSelected ? "destructive" : "outline"}
                  size="icon"
                  onClick={() => setIsBeingSelected(true)}
                >
                  <ListTodoIcon className="h-4 w-4 min-w-[40px]" />
                </Button>
              </TooltipTrigger>
              <TooltipContent side="left">Select chats</TooltipContent>
            </Tooltip>
        }
      </div>
      <ScrollArea>
        {
          filteredChats.length !== 0 ?
            <div className="h-full flex flex-col space-y-2 p-4 pt-0">
              {
                filteredChats.map((chatPreview) => (
                  <ChatItem
                    key={chatPreview.id}
                    chat={chatPreview}
                    isBeingSelected={isBeingSelected}
                    toggleSelect={() => { toggleOnSelect(chatPreview.id) }}
                  />
                ))
              }
            </div>
            :
            <div className="text-center text-muted-foreground">
              No chat found.
            </div>
        }
      </ScrollArea>
    </div >
  )
}